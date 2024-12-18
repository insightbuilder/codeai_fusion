import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = conn.channel()

channel.exchange_declare(exchange="dlx", exchange_type="direct")
channel.queue_declare(queue="dead_letter_queue", durable=True)
channel.queue_bind(exchange="dlx", queue="dead_letter_queue", routing_key="task_queue")

print(" [x] DLX and DLQ configured")

conn.close()
