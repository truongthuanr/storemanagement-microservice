import json
import pika
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
INVENTORY_QUEUE = os.getenv("INVENTORY_QUEUE", "inventory_queue")

def send_inventory_update(inventory_id: int, stock_change: int):
    message = {
        "type": "update_inventory",
        "inventory_id": inventory_id,
        "stock_change": stock_change,
    }

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    channel.queue_declare(queue=INVENTORY_QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=INVENTORY_QUEUE,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
