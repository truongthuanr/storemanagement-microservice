from pydantic import BaseModel, Field
from typing import Optional


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., example=101)
    quantity: int = Field(..., gt=0, example=3)


# 📤 Output trả về khi đọc order
class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_per_unit: float
    subtotal: float

    class Config:
        orm_mode = True
