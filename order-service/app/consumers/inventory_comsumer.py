import pika
import os
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
INVENTORY_RESPONSE_QUEUE = os.getenv("INVENTORY_RESPONSE_QUEUE", "order_inventory_response")

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"[x] Received inventory response: {message}")
    # Có thể xử lý thêm: log, update DB trạng thái, v.v.

def start_inventory_response_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()
    channel.queue_declare(queue=INVENTORY_RESPONSE_QUEUE, durable=True)

    channel.basic_consume(queue=INVENTORY_RESPONSE_QUEUE,
                          on_message_callback=callback,
                          auto_ack=True)

    print('[*] Waiting for inventory response messages. To exit press CTRL+C')
    channel.start_consuming()
