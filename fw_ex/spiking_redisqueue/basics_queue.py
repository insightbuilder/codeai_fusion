from rq import Queue
from redis import Redis
from tasks import process_data, fetch_url, long_running_task


# Connect to Redis
redis_conn = Redis(host="localhost", port=6379, db=0)

# Create an RQ queue
queue = Queue(connection=redis_conn)

# # Enqueue a task
# job = queue.enqueue(process_data, "example_data")
# print(f"Job ID: {job.id}")

urls = [
    "https://example.com",
    "https://httpbin.org",
    "https://jsonplaceholder.typicode.com/posts",
]
for url in urls:
    job = queue.enqueue(fetch_url, url)
    print(f"Enqueued job {job.id} for URL: {url}")

longjob = queue.enqueue(long_running_task, "tasm_021")
print(f"Job ID: {longjob.id}")
