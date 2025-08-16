# app/broker/rabbitmq.py
import aio_pika
import os
from aio_pika import ExchangeType

EXCHANGE_NAME = "order.exchange"

_connection = None
_channel = None
_exchange = None


async def get_connection():
    """Get or create a robust RabbitMQ connection."""
    global _connection
    if not _connection or _connection.is_closed:
        _connection = await aio_pika.connect_robust(
            os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
        )
    return _connection


async def get_channel():
    """Get or create a channel with QoS settings."""
    global _channel
    if not _channel or _channel.is_closed:
        conn = await get_connection()
        _channel = await conn.channel()
        await _channel.set_qos(prefetch_count=20)
    return _channel


async def setup_exchange(channel: aio_pika.Channel):
    """Declare (or reuse) the shared exchange."""
    global _exchange
    if not _exchange:
        _exchange = await channel.declare_exchange(
            EXCHANGE_NAME,
            ExchangeType.DIRECT,
            durable=True
        )
    return _exchange


async def close_connection():
    """Close channel and connection gracefully."""
    global _connection, _channel
    if _channel and not _channel.is_closed:
        await _channel.close()
    if _connection and not _connection.is_closed:
        await _connection.close()
