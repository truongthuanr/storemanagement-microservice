# app/events/consumer.py
import aio_pika, json, asyncio
from app.database import SessionLocal
from app.services import inventory_service as svc
from app.events.publisher import publish_event

async def _handle_order_created(msg: aio_pika.IncomingMessage):
    async with msg.process():
        data = json.loads(msg.body)
        order_id = data["order_id"]
        items = data["items"]                      # [{"id": .., "quantity": ..}, ...]

        db = SessionLocal()
        ok = svc.reserve_stock(db, items)
        db.close()

        await publish_event(
            "inventory.response",
            {"order_id": order_id, "status": "reserved" if ok else "failed"}
        )

async def consume():
    conn = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    ch = await conn.channel()
    queue = await ch.declare_queue("order.created", durable=True)
    await queue.consume(_handle_order_created)
    print("[MQ] Listening queue `order.created` …")
    return conn  # giữ reference để không bị đóng
