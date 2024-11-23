#!/bin/python

import grpc
from sqlmodel import except_
import add_grpc_pb2 as pb2
import add_grpc_pb2_grpc as pb2_grpc


def add_number(num1, num2):
    with grpc.insecure_channel("localhost:5055") as channel:
        stub = pb2_grpc.AddNumberStub(channel)
        request = pb2.AddRequest(num1=num1, num2=num2)
        response = stub.AddTwoNumber(request)
        print(f"The gRPC added number: {response.added}")


if __name__ == "__main__":
    while True:
        try:
            num1 = int(input("Enter first number: "))
            num2 = int(input("Enter second number: "))
            add_number(num1, num2)
        except Exception as e:
            print(f"{e}. Stopping")
            break
