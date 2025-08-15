import pytest
import aio_pika
import asyncio
import json

RABBIT_URL = "amqp://guest:guest@172.19.15.243:5672/"
ORDER_QUEUE = "order.created"
RESPONSE_QUEUE = "inventory.response"

@pytest.mark.asyncio
async def test_handle_order_created_success():
    conn = await aio_pika.connect_robust(RABBIT_URL)
    try:
        ch = await conn.channel()

        # Gửi message
        order_msg = {
            "event": "order.created",
            "timestamp": "2025-07-18T14:00:00Z",
            "correlation_id": "test-001",
            "producer": "test-suite",
            "data": {
                "order_id": "order_test_001",
                "user_id": 1,
                "items": [
                    {"product_id": 1, "quantity": 1},
                    {"product_id": 2, "quantity": 2}
                ]
            }
        }
        await ch.default_exchange.publish(
            aio_pika.Message(body=json.dumps(order_msg).encode()),
            routing_key=ORDER_QUEUE
        )

        # Lắng nghe phản hồi
        response_q = await ch.declare_queue(RESPONSE_QUEUE, durable=True)
        msg = await response_q.get(timeout=5)
        assert msg is not None

        response = json.loads(msg.body)
        assert response["data"]["order_id"] == "order_test_001"
        assert response["data"]["status"] in ["reserved", "failed"]

        # Optional: msg ack
        await msg.ack()

    finally:
        await conn.close()
