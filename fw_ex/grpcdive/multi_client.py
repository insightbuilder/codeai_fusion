#!/bin/python

from concurrent import futures
import random
from time import time
import grpc
import multi_service_pb2_grpc as pb2_grpc
import multi_service_pb2 as pb2
from argparse import ArgumentParser

parser_obj = ArgumentParser(
    prog="gRPC client",
    usage="""
multi_client -l : list existing persons
multi_client -p name1 25 location1 : create person
multi_client -g id : get person of that ID
""",
)

parser_obj.add_argument("-l", help="List the existing persons", action="store_true")
parser_obj.add_argument("-p", help="Create person in database", nargs=3)
parser_obj.add_argument("-g", help="Get person of id", nargs="?")
parser_obj.add_argument("-d", help="Delete person by id", nargs="?")

args_parsed = parser_obj.parse_args()
print(args_parsed.l)
print(args_parsed.p)
print(args_parsed.g)
print(args_parsed.d)


def get_list():
    with grpc.insecure_channel("localhost:5055") as chn:
        stub = pb2_grpc.PersonServiceStub(chn)
        response = stub.ListPersons(pb2.Empty())
        for idx, res in enumerate(response):
            print(f"Person: {idx}")
            print("###############")
            print(f"Person name: {res.name}")
            print(f"Person location: {res.location}")
            print("################")


def create_person(name, age, location):
    age = int(age)
    with grpc.insecure_channel("localhost:5055") as chn:
        stub = pb2_grpc.PersonServiceStub(chn)
        person = pb2.CreatePersonRequest(name=name, age=age, location=location)
        response = stub.CreatePerson(person)
        print(f"Person: {response.id}")
        print("###############")
        print(f"{response.message}")


def create_delete_loop():
    import numpy as np

    create_times = []
    delete_times = []

    with grpc.insecure_channel(
        "ec2-54-198-243-221.compute-1.amazonaws.com:5055"
    ) as chn:
        stub = pb2_grpc.PersonServiceStub(chn)
        for out in range(0, 5):
            print(f"Starting {out + 1} create delete loop")
            c_str = time()
            for idx in range(0, 50):
                name = f"name_{idx}"
                location = f"location_{idx}"
                age = random.randint(25, 50)
                person = pb2.CreatePersonRequest(name=name, age=age, location=location)
                cres = stub.CreatePerson(person)
                print(f"request_{idx}: {cres.message}")

            c_end = time()
            create_times.append(c_end - c_str)

            d_str = time()
            for idx in range(1, 51):
                req = pb2.PersonIdRequest(id=idx)
                dres = stub.DeletePersonById(req)
                print(f"del_req_{idx}: {dres.status}")
            d_end = time()
            delete_times.append(d_end - d_str)

    print(f"create_times: {create_times}")
    c_mtime = np.array(create_times).mean()
    print(f"create_mean: {c_mtime}")

    print(f"delete_times: {delete_times}")
    d_mtime = np.array(delete_times).mean()
    print(f"delete_mean: {d_mtime}")

    print("Any left out persons")
    get_list()


def get_person(gid):
    with grpc.insecure_channel("localhost:5055") as chn:
        stub = pb2_grpc.PersonServiceStub(chn)
        req = pb2.PersonIdRequest(id=gid)
        person = stub.GetPersonById(req)
        print(f"Person: {person.name}")
        print("###############")
        print(f"Age:{person.age}")
        print("###############")
        print(f"Location:{person.location}")


def delete_person(gid):
    with grpc.insecure_channel("localhost:5055") as chn:
        stub = pb2_grpc.PersonServiceStub(chn)
        req = pb2.PersonIdRequest(id=gid)
        person = stub.DeletePersonById(req)
        print(f"Delete Request: {person.status}")


if args_parsed.l:
    get_list()

elif args_parsed.p:
    create_person(args_parsed.p[0], args_parsed.p[1], args_parsed.p[2])

elif args_parsed.g:
    gid = int(args_parsed.g)
    get_person(gid)

elif args_parsed.d:
    gid = int(args_parsed.d)
    delete_person(gid)

else:
    create_delete_loop()
