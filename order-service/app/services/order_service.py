from sqlalchemy.orm import Session
from app import crud, schemas
from uuid import uuid4
from app.models import Order, OrderItem, OrderCreate, OrderStatusEnum
# from app.producers.inventory_producer import send_inventory_update
from app.exceptions import OrderValidationError, ProductUnavailable
from datetime import datetime, timezone
from app.brokers import publish_order_created
from app.servicelogging import logger

# Message format
# {
# "event": "order.created",
# "timestamp": "2025-07-18T14:00:00Z",
# "correlation_id": "abc123-xyz789",
# "producer": "order-service",
# "data": {
#     "order_id": "order_001",
#     "user_id": 123,
#     "items": [
#     { "product_id": 1, "quantity": 2 },
#     { "product_id": 2, "quantity": 1 }
#     ]
# }
# }
async def create_order_service(request: Request, payload: OrderCreate, db: Session) -> dict:
    logger.info(f"Start create_order_service for customer_id={payload.customer_id} with {len(payload.items)} items.")

    if not payload.items:
        raise OrderValidationError("Order must contain at least one item")

    # Step 1: Create Order with status init
    order = Order(
        customer_id=payload.customer_id,
        status=OrderStatusEnum.init.value,
        created_at=datetime.now(timezone.utc)
    )
    db.add(order)
    db.flush()
    logger.info(f"Created order with id={order.id}, status={order.status}")

    # Step 2: Ghi OrderItems
    for item in payload.items:
        db_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_unit=None
        )
        db.add(db_item)
    db.commit()
    logger.info(f"Committed order and items to DB for order_id={order.id}")

    # Step 3: Tạo message và gửi
    correlation_id = str(uuid4())
    message = {
        "event": "order.created",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "correlation_id": correlation_id,
        "producer": "order-service",
        "data": {
            "order_id": str(order.id),
            "user_id": payload.customer_id,
            "items": [
                {"product_id": item.product_id, "quantity": item.quantity}
                for item in payload.items
            ]
        }
    }

    logger.info(f"Publishing order.created message for order_id={order.id}, correlation_id={correlation_id}")
    await publish_order_created(request.app, message)
    logger.info(f"Message published successfully for order_id={order.id}")

    return {
        "order_id": order.id,
        "status": order.status,
        "correlation_id": correlation_id
    }


def get_order(db: Session, order_id: int) -> Order:
    return crud.order.get_order(db, order_id)

def list_orders(db: Session):
    return crud.order.list_orders(db)

def delete_order(db: Session, order_id: int) -> bool:
    return crud.order.delete_order(db, order_id)
