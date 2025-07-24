from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class InventoryItemResult(BaseModel):
    product_id: int
    price: float


class InventoryResponseMessage(BaseModel):
    event: Literal["inventory.response"]
    timestamp: datetime
    correlation_id: str
    producer: str = "inventory-service"
    order_id: str
    status: Literal["reserved", "failed"]
    items: List[InventoryItemResult]
    reason: Optional[str] = None
