import grpc
import test_pb2
import test_pb2_grpc

def run():
    # Open a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = test_pb2_grpc.TestServiceStub(channel)
        while True:
            s = input("Enter string to send: ")
            print(f'Sending {s}')
            for _ in range(10):
                response = stub.SayHello(test_pb2.HelloRequest(name=s))
                print(f"Client received: {response.message}")

if __name__ == "__main__":
    run()
