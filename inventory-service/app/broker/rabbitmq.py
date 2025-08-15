# app/broker/rabitmq.py
import aio_pika
import os

_connection = None
_channel = None

async def get_connection():
    global _connection
    if not _connection or _connection.is_closed:
        _connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/"))
    return _connection

async def get_channel():
    global _channel
    if not _channel or _channel.is_closed:
        conn = await get_connection()
        _channel = await conn.channel()
    return _channel
