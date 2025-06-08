from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Tạo base cho các mô hình
Base = declarative_base()

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    # Quan hệ với bảng khác nếu cần (ví dụ, Category, nếu có)
    # category_id = Column(Integer, ForeignKey('categories.id'))
    # category = relationship("Category", back_populates="products")
