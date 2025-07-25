<<<<<<< Updated upstream
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
=======
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
>>>>>>> Stashed changes
