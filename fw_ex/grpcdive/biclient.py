from __future__ import print_function

import grpc
import biderection_pb2_grpc as pb2_grpc
import biderection_pb2 as pb2


def make_message(message):
    return pb2.Message(message=message)


def generate_message():
    messages = [
        make_message("First"),
        make_message("Second"),
        make_message("Third"),
        make_message("South"),
    ]
    for msg in messages:
        print(f"Client sending {msg}")
        yield msg


def send_msg(stub):
    response = stub.GetServerResponse(generate_message())
    for res in response:
        print(f"Okay, I am server sending: {res.message}")


def interact():
    with grpc.insecure_channel("localhost:50551") as channel:
        stub = pb2_grpc.BidirectionalStub(channel)
        send_msg(stub)


if __name__ == "__main__":
    interact()
