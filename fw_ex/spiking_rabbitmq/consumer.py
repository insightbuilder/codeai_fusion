import pika
import time


def process_task(ch, method, properties, body):
    """Process a task from RabbitMQ."""
    body = body.decode()
    print(f" [x] Received message: {body}")
    time.sleep(5)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consuming():
    """Consume messages from RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    print("[*] Waiting for the tasks [*]")
    channel.basic_qos(prefetch_count=1)
    # here the process happens in callback function
    channel.basic_consume(
        queue="hello", on_message_callback=process_task, auto_ack=False
    )
    channel.start_consuming()


if __name__ == "__main__":
    consuming()
