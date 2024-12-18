import pika

# Connection setup
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# Declare the DLQ
channel.queue_declare(queue="dead_letter_queue", durable=True)


def dlq_callback(ch, method, properties, body):
    print(f" [☠] Dead-Lettered Message: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="dead_letter_queue", on_message_callback=dlq_callback)

print(" [*] Waiting for DLQ messages. To exit, press CTRL+C")
channel.start_consuming()
