import grpc
from concurrent import futures
import time
import unary_pb2_grpc as pb2_grpc
import unary_pb2 as pb2


class UnaryService(pb2_grpc.UnaryServicer):
    def __init__(self) -> None:
        pass

    # below method is actually not required, but
    # the add_UnaryServicer_to_server is asking for a UnaryServicer obj
    # so wrapping it inside it, and this is already defined in unary.proto
    def GetServerResponse(self, request, context):
        # request contains the message
        message = request.message
        ctx = context
        result = f"Hi I am up. Recieved message {message}"
        print(f"Context is: {ctx}")
        result = {"message": result, "recieved": True}
        return pb2.MessageResponse(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc.add_UnaryServicer_to_server(UnaryService(), server)
    server.add_insecure_port("[::]:50551")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
