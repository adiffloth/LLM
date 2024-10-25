import grpc
from concurrent import futures
import test_pb2
import test_pb2_grpc

# Implement the service defined in the proto file
class TestServiceServicer(test_pb2_grpc.TestServiceServicer):
    def SayHello(self, request, context):
        print(f'Received request {request.name}')
        return test_pb2.HelloReply(message=f"Hello, {request.name}!")

# Start the server
def serve():
    print('Starting server')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_TestServiceServicer_to_server(TestServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
