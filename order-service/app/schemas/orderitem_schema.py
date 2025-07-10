from pydantic import BaseModel, Field
from typing import Optional


class OrderItemCreate(BaseModel):
    inventory_id: int = Field(..., example=101)
    quantity: int = Field(..., gt=0, example=3)
    price_per_unit: float = Field(..., gt=0, example=12000.5)


class OrderItemRead(BaseModel):
    id: int
    inventory_id: int
    quantity: int
    price_per_unit: float
    subtotal: float

    class Config:
        orm_mode = True
