import grpc
import unary_pb2_grpc as pb2_grpc
import unary_pb2 as pb2


class UnaryClient:
    """
    Client for gRPC functionality
    """

    def __init__(self) -> None:
        self.host = "localhost"
        self.port = 50551

        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.stub = pb2_grpc.UnaryStub(self.channel)

    def get_url(self, message):
        """
        Client method to call the gRPC server
        """

        message = pb2.Message(message=message)
        print(f"{message} sent")
        return self.stub.GetServerResponse(message)


if __name__ == "__main__":
    client = UnaryClient()
    while True:
        your_input = input("Provide some input: ")
        if your_input == "exit" or your_input == "":
            print("See ya")
            break
        result = client.get_url(message=your_input)
        print(f"{result} is the result")
