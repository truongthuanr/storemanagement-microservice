from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    inventory_id = Column(Integer, nullable=False)  # liên kết tới Inventory
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)  # quantity * price_per_unit

    order = relationship("Order", back_populates="items")
