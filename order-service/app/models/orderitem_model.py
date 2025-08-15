from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, nullable=False)  # liên kết tới Inventory
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=True)  # Có thể null trước khi cập nhật giá
    subtotal = Column(Float, nullable=True)        # quantity * price_per_unit, cũng có thể null

    order = relationship("Order", back_populates="items")

