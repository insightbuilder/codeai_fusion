#!/bin/python

import requests
import random

base_url = "http://ec2-54-198-243-221.compute-1.amazonaws.com:8000/"


def create_persons():
    create = f"{base_url}person/add"
    for idx in range(0, 50):
        pdt = dict(
            name=f"name_{idx}",
            age=random.randrange(10, 20),
            location=f"location_{idx}",
        )
        res1 = requests.post(url=create, json=pdt)
        print(f"Result of {idx}: {res1.status_code}")


def delete_persons():
    delete = f"{base_url}person/"
    for idx in range(1, 51):
        del1 = requests.delete(url=f"{delete}{idx}")
        print(f"Result of {idx}: {del1.status_code}")


def all_products():
    all = f"{base_url}person/all"
    resall = requests.get(url=all)
    print("Print all: \n", resall.json())


# resall = requests.get(url=all)
# print("Print all: \n", resall.json())  # print(pdt_json)

if __name__ == "__main__":
    import time
    import numpy as np

    create_times = []
    delete_times = []

    for t in range(0, 5):
        print(f"Creating {t} set")
        c_str = time.time()
        create_persons()
        c_end = time.time()
        # storing the time taken to create
        create_times.append(c_end - c_str)
        print(f"Deleting {t} set")
        d_str = time.time()
        delete_persons()
        d_end = time.time()
        # storing the time taken to create
        delete_times.append(d_end - d_str)

    create_mean = np.array(create_times).mean()
    delete_mean = np.array(delete_times).mean()

    print(f"Mean create times: {create_mean}")
    print(f"create times: {create_times}")
    print(f"Mean delete times: {delete_mean}")
    print(f"delete times: {delete_times}")

    all_products()
