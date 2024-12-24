import requests
import time


def process_data(data):
    print(f"Processing data: {data}")
    return f"Processed {data}"


def fetch_url(url):
    print(f"Fetching {url}")
    response = requests.get(url)
    return response.text[:100]  # Return the first 100 characters


def long_running_task(task_id):
    print(f"Starting task {task_id}")
    time.sleep(500)  # Simulate a long task
    print(f"Completed task {task_id}")
    return f"Task {task_id} finished"
