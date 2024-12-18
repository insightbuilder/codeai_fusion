import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

args = {
    "x-dead-letter-exchange": "dlx",
    "x-message-ttl": 5000,
}

channel.queue_declare(queue="task_queue", durable=True, arguments=args)

for i in range(10):
    message = f"Publishing file_{i}.jpg"
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )
    # File path has been sent out.
    print(f" [x] sent {message}")

connection.close()
