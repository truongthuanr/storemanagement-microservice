# app/services/inventory_service.py
from __future__ import annotations
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, declarative_base, Session


from app.database import SessionLocal
from app.crud import inventory_crud
from app.servicelogging.servicelogger import logger
from app.schemas.inventory_response import InventoryResponseMessage, InventoryItemResult
from app.broker.publisher import publish_event


# ---------- Helpers -------------------------------------------------
def _to_dict(model) -> Dict:
    return {
        "id": model.id,
        "name": model.name,
        "description": model.description or "",
        "product_id":model.product_id,
        "price": float(model.price),
        "stock": model.stock,
        "created_at": model.created_at,
        "updated_at": model.updated_at,
    }


# ---------- CRUD-style services ------------------------------------
def list_inventory(db: Session) -> List[Dict]:
    return [_to_dict(i) for i in inventory_crud.get_all_inventory(db)]


def get_inventory(db: Session, inv_id: int) -> Optional[Dict]:
    m = inventory_crud.get_inventory_by_id(db, inv_id)
    return _to_dict(m) if m else None

def get_stock_by_productid(db: Session, product_id) -> int:
    return inventory_crud.get_stock_by_productid(db, product_id)

def create_inventory(db: Session, *, product_id: int, name: str, description: str, price: float, stock: int) -> Dict:
    logger.info("Function Start!")
    m = inventory_crud.create_inventory(db, product_id, name, description, price, stock)
    result =  _to_dict(m)
    
    logger.info(
        f"Return | "
        f"product_id={product_id}, name={name}, price={price}, stock={stock}, id={result['id']}, description={description}"
    )
    
    return result


def update_inventory(db: Session, inv_id: int, **fields) -> Optional[Dict]:
    m = inventory_crud.update_inventory(db, inv_id, **fields)
    return _to_dict(m) if m else None


def delete_inventory(db: Session, inv_id: int) -> bool:
    return inventory_crud.delete_inventory(db, inv_id)


# ---------- Domain logic used by Order -----------------------------
def reserve_stock(db: Session, items: List[Dict]) -> Tuple[bool, List[Dict], Optional[str]]:
    """
    items = [{"product_id": int, "quantity": int}, ...]
    Returns:
        ok (bool) - True if stock is sufficient and reserved, False if insufficient
        reserved_items (list) - List of successfully reserved products
        reason (str|None) - Failure reason (if any)
    """
    logger.info("Function start!")
    reserved_items = []
    reason = None

    # 1. Kiểm tra đủ hàng
    logger.info("Check each item")
    for it in items:
        m = inventory_crud.get_stock_by_productid(db, it["product_id"])
        if not m or m < it["quantity"]:
            logger.info(
                f"Insufficient stock for item_id={it['product_id']}: "
                f"requested={it['quantity']}, available={m if m else 'None'}"
            )
            reason = f"Insufficient stock for product_id={it['product_id']}"
            return False, reserved_items, reason

    # 2. Reserve stock
    for it in items:
        m = inventory_crud.get_stock_by_productid(db, it["product_id"])
        inventory_crud.update_inventory(db, it["product_id"], stock=m - it["quantity"])
        reserved_items.append({
            "product_id": it["product_id"],
            "quantity": it["quantity"]
        })

    logger.info("Stock check passed for all items.")
    return True, reserved_items, reason

async def handle_order_created(payload: dict, correlation_id: str):
    order_id = payload["order_id"]
    items = payload["items"]

    db = SessionLocal()
    try:
        ok, reserved_items, reason = reserve_stock(db, items)
    finally:
        db.close()

    msg = InventoryResponseMessage(
        event="order.inventory_reserved",
        timestamp=datetime.now(timezone.utc),
        correlation_id=correlation_id,
        producer="inventory-service",
        order_id=order_id,
        status="reserved" if ok else "failed",
        items=[InventoryItemResult(**item) for item in reserved_items],
        reason=reason
    )

    await publish_event("order.inventory_reserved", msg.model_dump())