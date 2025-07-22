# app/events/consumer.py
import aio_pika, json, asyncio
from app.database import SessionLocal
from app.services import inventory_service as svc
from app.events.publisher import publish_event
from aio_pika import ExchangeType

from app.servicelogging.servicelogger import logger


async def _handle_order_created(msg: aio_pika.IncomingMessage):
    '''
        format message:
        {
        "event": "order.created",
        "timestamp": "2025-07-18T14:00:00Z",
        "correlation_id": "abc123-xyz789",
        "producer": "order-service",
        "data": {
            "order_id": "order_001",
            "user_id": 123,
            "items": [
            { "product_id": 1, "quantity": 2 },
            { "product_id": 2, "quantity": 1 }
            ]
        }
        }
    '''
    logger.info("Function start!")
    async with msg.process():
        try:
            message = json.loads(msg.body)
            logger.info(f"message={message}")

            # Lấy phần metadata và payload
            correlation_id = message["correlation_id"]
            event = message["event"]
            payload = message["data"]             # phần chứa order_id, items
            order_id = payload["order_id"]
            items = payload["items"]              # [{"product_id": 1, "quantity": 2}, ...]

            # Thực hiện giữ hàng
            db = SessionLocal()
            ok = svc.reserve_stock(db, items)
            logger.info(f"Reserve stock status: {ok}")
            db.close()

            # Gửi phản hồi: inventory.response
            logger.info(f"Publish event order_id={order_id}, status={'reserved' if ok else 'failed'}")
            await publish_event(
                    routing_key="inventory.response",
                    event="inventory.reserved",
                    data={
                        "order_id": order_id,
                        "status": "reserved" if ok else "failed"
                    },
                    correlation_id=correlation_id,
                    producer="inventory-service"
                )
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            print(f"[ERROR] Failed to process message: {e}")


async def consume():
    conn = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    ch = await conn.channel()

    # Declare exchange
    exchange = await ch.declare_exchange("order.exchange", ExchangeType.DIRECT, durable=True)

    # Declare queue & bind vào exchange với routing key
    queue = await ch.declare_queue("order.created", durable=True)
    await queue.bind(exchange, routing_key="order.created")

    # Consume
    await queue.consume(_handle_order_created)
    print("[MQ] Listening queue `order.created` …")

    return conn
