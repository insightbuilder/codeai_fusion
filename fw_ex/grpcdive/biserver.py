from concurrent import futures
import grpc
import biderection_pb2_grpc as pb2_grpc
from biclient import make_message


class BidirectionService(pb2_grpc.BidirectionalServicer):
    def GetServerResponse(self, request_iterator, context):
        for message in request_iterator:
            prc_msg = f"I processed: {message}"
            yield make_message(message=prc_msg)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc.add_BidirectionalServicer_to_server(BidirectionService(), server)
    server.add_insecure_port("[::]:50551")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
