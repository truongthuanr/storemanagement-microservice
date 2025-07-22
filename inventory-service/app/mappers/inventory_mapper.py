from app.proto.inventory_pb2 import InventoryItem
from decimal import Decimal
from datetime import datetime

def to_proto_item(d: dict) -> InventoryItem:
    return InventoryItem(
        id=int(d["id"]),
        product_id=int(d["product_id"]),
        name=str(d["name"]),
        description=str(d["description"] or ""),  # fallback nếu là None
        price=float(d["price"]) if isinstance(d["price"], (float, Decimal)) else 0.0,
        stock=int(d["stock"]),
        created_at=_to_iso(d.get("created_at")),
        updated_at=_to_iso(d.get("updated_at")),
    )

def _to_iso(value) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if value is None:
        return ""
    return str(value)
