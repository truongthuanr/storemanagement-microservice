# app/services/inventory_service.py
from __future__ import annotations
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, declarative_base, Session


from app.database import SessionLocal
from app.crud import inventory_crud
from app.servicelogging.servicelogger import logger
from app.schemas.inventory_response import InventoryResponseMessage, InventoryItemResult, ReserveStockResult
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
def reserve_stock(db: Session, items: List[Dict]) -> ReserveStockResult:
    """
    items = [{"product_id": int, "quantity": int}, ...]
    """
    logger.info("▶️ reserve_stock function start")
    reserved_items: List[InventoryItemResult] = []
    for it in items:
        logger.info(f"🔍 Checking product_id={it['product_id']} with requested quantity={it['quantity']}")

        _inventory = inventory_crud.get_inventory_by_product_id(db, product_id=it["product_id"])
        logger.debug(f"_inventory: {_inventory}")
        if not _inventory:
            reason = f"❌ Product not found: product_id={it['product_id']}"
            logger.warning(reason)
            return ReserveStockResult(ok=False, reserved_items=[], reason=reason)

        logger.debug(
            f"Available stock={_inventory.stock}, unit_price={_inventory.price} "
            f"for product_id={it['product_id']}"
        )

        if _inventory.stock < it["quantity"]:
            reason = (
                f"❌ Insufficient stock for product_id={it['product_id']}: "
                f"requested={it['quantity']}, available={_inventory.stock}"
            )
            logger.warning(reason)
            return ReserveStockResult(ok=False, reserved_items=[], reason=reason)

        # Reserve stock
        new_stock = _inventory.stock - it["quantity"]
        inventory_crud.update_inventory(db, _inventory.id, stock=new_stock)
        logger.info(
            f"✅ Reserved product_id={it['product_id']}, quantity={it['quantity']}, "
            f"new_stock={new_stock}"
        )

        reserved_items.append(
            InventoryItemResult(
                product_id=it["product_id"],
                quantity=it["quantity"],
                unit_price=_inventory.price
            )
        )

    logger.info("🎉 Stock check passed for all items, reservation successful.")
    return ReserveStockResult(ok=True, reserved_items=reserved_items)



async def handle_order_created(payload: dict, correlation_id: str):
    order_id = payload["order_id"]
    items = payload["items"]

    db = SessionLocal()
    try:
        result = reserve_stock(db, items)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.exception(f"❌ Error reserving stock for order_id={order_id}")
        raise
    finally:
        db.close()

    msg = InventoryResponseMessage(
        event="order.inventory_reserved",
        timestamp=datetime.now(timezone.utc),
        correlation_id=correlation_id,
        producer="inventory-service",
        order_id=order_id,
        status="reserved" if result.ok else "failed",
        items=result.reserved_items,   # list[InventoryItemResult]
        reason=result.reason
    )

    await publish_event("order.inventory_reserved", msg.model_dump())
    logger.info(f"📤 Sent inventory response for order_id={order_id}, status={msg.status}")