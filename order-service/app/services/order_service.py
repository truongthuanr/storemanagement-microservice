from sqlalchemy.orm import Session
from app import crud, schemas
from app.models import Order, OrderItem
from app.producers.inventory_producer import send_inventory_update

def create_order(db: Session, order_data: schemas.OrderCreate) -> Order:
    order = crud.order.create_order(db, order_data)
    
    for item in order.items:
        send_inventory_update(inventory_id=item.inventory_id, stock_change=-item.quantity)

    return order

def get_order(db: Session, order_id: int) -> Order:
    return crud.order.get_order(db, order_id)

def list_orders(db: Session):
    return crud.order.list_orders(db)

def delete_order(db: Session, order_id: int) -> bool:
    return crud.order.delete_order(db, order_id)
