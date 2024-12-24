from rq.job import Job
from redis import Redis

redis_conn = Redis(host="localhost", port=6379, db=0)
# job = Job.fetch("918920fb-dd8d-4c2f-9f47-b0f3b024685a", connection=redis_conn)
job = Job.fetch(
    # "b7348204-097a-484f-abf0-bbffdd4d177a",
    # "4f152f61-02a4-434d-9207-a2c905ef518a",
    # "26e3d11a-4a25-401b-ac59-6cf96a5631b3",
    "4a9cdd52-bdd1-4f4f-aed2-77be687bc063",
    connection=redis_conn,
)

print(f"Job Status: {job.get_status()}")
if job.is_finished:
    print(f"Result: {job.result}")
