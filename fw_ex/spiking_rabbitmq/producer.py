import pika


def send_task(message):
    """Send a message to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    # Declare a queue
    channel.queue_declare(queue="hello")
    # Publish a message to the hello queue with routing key "hello"
    channel.basic_publish(
        exchange="",
        routing_key="hello",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),  # make message persistant
    )

    print(" [x] Sent %r" % message)
    connection.close()
