import pika
import time
import random

RETRY_LIMIT = 3

conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = conn.channel()

channel.queue_declare(
    queue="task_queue",
    durable=True,
    arguments={"x-message-ttl": 5000, "x-dead-letter-exchange": "dlx"},
)


def process_me(body):
    """Simulate image processing"""
    print(f" [x] processing: {body.decode()}")

    time.sleep(2)
    if random.choice([True, False]):
        raise Exception("Image processing failed")


def callback(ch, method, properties, body):
    """Consumer callback to process messages."""
    try:
        process_me(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Done: {body.decode()}")
    except Exception as e:
        print(f" [x] Error: {e}")

        headers = properties.headers or {}
        retry_count = headers.get("x-retry-count", 0)

        if retry_count < RETRY_LIMIT:
            print(f" [x] Retrying: {body.decode()}")
            ch.basic_publish(
                exchange="",
                routing_key="task_queue",
                body=body,
                properties=pika.BasicProperties(
                    headers={"x-retry-count": retry_count + 1}, delivery_mode=2
                ),
            )
        else:
            print(f" [x] Moving to dlq: {body.decode()}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
