from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class InventoryItemResult(BaseModel):
    product_id: int
    quantity: int
    unit_price: Optional[float] = None

class InventoryResponseMessage(BaseModel):
    event: Literal["order.inventory_reserved"]
    timestamp: datetime
    correlation_id: str
    producer: str = "inventory-service"
    order_id: str
    status: Literal["reserved", "failed"]
    items: List[InventoryItemResult]
    reason: Optional[str] = None

class ReserveStockResult(BaseModel):
    ok: bool
    reserved_items: List[InventoryItemResult] = []
    reason: Optional[str] = None