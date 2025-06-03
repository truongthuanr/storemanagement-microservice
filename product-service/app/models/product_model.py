from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    category = Column(String(100))
