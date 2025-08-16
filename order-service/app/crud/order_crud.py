from sqlalchemy.orm import Session
from app.models.order_model import Order, OrderStatusEnum
from app.models.orderitem_model import OrderItem
from app.schemas.order_schema import OrderCreate
from app.schemas.orderitem_schema import OrderItemCreate
from typing import List

def create_order(db: Session, order_data: OrderCreate) -> Order:
    order = Order(
        customer_id=order_data.customer_id,
        status=OrderStatusEnum.pending,
        total_amount=0.0  # tạm tính, sẽ cập nhật sau
    )
    db.add(order)
    db.flush()  # để có order.id dùng cho OrderItems

    total = 0.0
    items = []
    for item_data in order_data.items:
        subtotal = item_data.quantity * item_data.price_per_unit
        total += subtotal
        item = OrderItem(
            order_id=order.id,
            inventory_id=item_data.inventory_id,
            quantity=item_data.quantity,
            price_per_unit=item_data.price_per_unit,
            subtotal=subtotal
        )
        items.append(item)

    order.total_amount = total
    db.add_all(items)
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()

def update_order_status(db: Session, order_id: int, status: OrderStatusEnum) -> Order | None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int) -> bool:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True


def get_all_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).offset(skip).limit(limit).all()


def set_order_status(db: Session, order_id: int, success: bool, reason: str = None):
    """
    Update only the order status.
    """
    order = get_order(db, order_id)
    if not order:
        return None

    if success:
        order.status = OrderStatusEnum.confirmed.value
    else:
        order.status = OrderStatusEnum.cancelled.value

    db.add(order)
    return order