# app/services/inventory_service.py
from __future__ import annotations
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from app.crud import inventory_crud


# ---------- Helpers -------------------------------------------------
def _to_dict(model) -> Dict:
    return {
        "id": model.id,
        "name": model.name,
        "description": model.description or "",
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


def create_inventory(db: Session, *, name: str, description: str, price: float, stock: int) -> Dict:
    m = inventory_crud.create_inventory(db, name, description, price, stock)
    return _to_dict(m)


def update_inventory(db: Session, inv_id: int, **fields) -> Optional[Dict]:
    m = inventory_crud.update_inventory(db, inv_id, **fields)
    return _to_dict(m) if m else None


def delete_inventory(db: Session, inv_id: int) -> bool:
    return inventory_crud.delete_inventory(db, inv_id)


# ---------- Domain logic used bởi Order -----------------------------
def reserve_stock(db: Session, items: List[Dict]) -> bool:
    """
    items = [{"id": int, "quantity": int}, ...]
    Trả True nếu đủ hàng & đã trừ, False nếu thiếu.
    """
    # 1. Kiểm tra đủ hàng
    for it in items:
        m = inventory_crud.get_inventory_by_id(db, it["id"])
        if not m or m.stock < it["quantity"]:
            return False
    # 2. Trừ kho
    for it in items:
        inventory_crud.update_inventory(db, it["id"], stock=m.stock - it["quantity"])
    return True
