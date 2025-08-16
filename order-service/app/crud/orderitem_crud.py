from sqlalchemy.orm import Session
from app.models.orderitem_model import OrderItem
from app.schemas.orderitem_schema import OrderItemCreate
from typing import List, Optional


def create_order_item(db: Session, order_id: int, item_data: OrderItemCreate) -> OrderItem:
    subtotal = item_data.quantity * item_data.price_per_unit
    item = OrderItem(
        order_id=order_id,
        inventory_id=item_data.inventory_id,
        quantity=item_data.quantity,
        price_per_unit=item_data.price_per_unit,
        subtotal=subtotal
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: int) -> Optional[OrderItem]:
    return db.query(OrderItem).filter(OrderItem.id == item_id).first()


def get_items_by_order(db: Session, order_id: int) -> List[OrderItem]:
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


def update_order_item(
    db: Session,
    item_id: int,
    quantity: Optional[int] = None,
    price_per_unit: Optional[float] = None
) -> Optional[OrderItem]:
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not item:
        return None
    if quantity is not None:
        item.quantity = quantity
    if price_per_unit is not None:
        item.price_per_unit = price_per_unit
    item.subtotal = item.quantity * item.price_per_unit
    db.commit()
    db.refresh(item)
    return item


def delete_order_item(db: Session, item_id: int) -> bool:
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

def update_reserved_items(db: Session, order_id: int, reserved_items: list):
    """
    Update prices and subtotals for reserved items.
    """
    for reserved in reserved_items:
        db_item = (
            db.query(OrderItem)
            .filter(
                OrderItem.order_id == order_id,
                OrderItem.product_id == reserved["product_id"]
            )
            .first()
        )
        if db_item:
            db_item.price_per_unit = reserved["price_per_unit"]
            db_item.subtotal = db_item.price_per_unit * db_item.quantity
            db.add(db_item)
