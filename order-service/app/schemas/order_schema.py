from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from enum import Enum
from app.schemas.orderitem_schema import OrderItemCreate, OrderItemRead


class OrderStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class OrderCreate(BaseModel):
    customer_id: int = Field(..., example=1)
    items: List[OrderItemCreate]


class OrderRead(BaseModel):
    id: int
    customer_id: int
    status: OrderStatusEnum
    total_amount: float
    created_at: datetime
    updated_at: datetime | None = None
    items: List[OrderItemRead]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum
