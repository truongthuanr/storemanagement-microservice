# models/product_price.py
from sqlalchemy import Column, Integer, Float, DateTime
from app.database import Base
from datetime import datetime

class ProductPrice(Base):
    __tablename__ = "product_price"

    product_id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
