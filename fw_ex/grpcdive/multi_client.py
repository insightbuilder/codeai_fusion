#!/bin/python

from concurrent import futures
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
args_parsed = parser_obj.parse_args()
print(args_parsed.l)
print(args_parsed.p)
print(args_parsed.g)


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


if args_parsed.l:
    get_list()

elif args_parsed.p:
    create_person(args_parsed.p[0], args_parsed.p[1], args_parsed.p[2])

elif args_parsed.g:
    gid = int(args_parsed.g)
    get_person(gid)
