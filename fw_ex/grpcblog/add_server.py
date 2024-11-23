import grpc
from concurrent import futures
import add_grpc_pb2 as pb2
import add_grpc_pb2_grpc as pb2_grpc


class AddingNumbers(pb2_grpc.AddNumberServicer):
    def AddTwoNumber(self, request, context):
        num1 = request.num1
        num2 = request.num2
        added = num1 + num2
        return pb2.AddResponse(added=added)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc.add_AddNumberServicer_to_server(AddingNumbers(), server)
    server.add_insecure_port("[::]:5055")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
