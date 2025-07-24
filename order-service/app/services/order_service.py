from sqlalchemy.orm import Session
from app import crud, schemas
from app.models import Order, OrderItem, OrderCreate, OrderStatusEnum
# from app.producers.inventory_producer import send_inventory_update
from app.exceptions import OrderValidationError, ProductUnavailable
from datetime import datetime, timezone
from app.brokers import publish_order_created
from app.servicelogging import logger
# Message format
# {
#   "event": "order.created",
#   "timestamp": "2025-07-23T21:15:30Z",
#   "order_id": "ord_123456",
#   "customer_id": "cus_7890",
#   "items": [
#     {
#       "product_id": 101,
#       "quantity": 2
#     },
#     {
#       "product_id": 202,
#       "quantity": 1
#     }
#   ]
# }
async def create_order_service(payload: OrderCreate, db: Session) -> dict:
    logger.info(f"Create order start!")
    if not payload.items:
        raise OrderValidationError("Order must contain at least one item")

    # Step 1: Create Order with status init
    order = Order(
        customer_id=payload.customer_id,
        status=OrderStatusEnum.init.value,  # trạng thái khởi tạo
        created_at=datetime.now()
    )
    db.add(order)
    db.flush()  # để lấy order.id
    logger.info(f"Order created with order_id={order.id}")

    # Step 2: Ghi OrderItem ở trạng thái "chờ giá"
    for item in payload.items:
        db_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_unit=None  # sẽ cập nhật sau khi nhận từ inventory
        )
        db.add(db_item)

    db.commit()

    # Step 3: Gửi message tới Inventory để reserve + lấy giá
    message = {
        "event": "order.created",
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "order_id": order.id,
        "customer_id": payload.customer_id,
        "items": [
            {"product_id": item.product_id, "quantity": item.quantity}
            for item in payload.items
        ]
    }
    logger.info(f"Message created: {message}")
    await publish_order_created(message)

    logger.info(f"Successfully create order order_id={order.id}, status={order.status}")
    return {
        "order_id": order.id,
        "status": order.status
    }


def get_order(db: Session, order_id: int) -> Order:
    return crud.order.get_order(db, order_id)

def list_orders(db: Session):
    return crud.order.list_orders(db)

def delete_order(db: Session, order_id: int) -> bool:
    return crud.order.delete_order(db, order_id)
