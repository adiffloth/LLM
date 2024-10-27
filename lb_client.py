import grpc
import streaming_pb2
import streaming_pb2_grpc
import time
import sys

def generate_data_chunks(client_id):
    # Simulate sending a stream of data
    for i in range(1, 21):  # Send 20 chunks of data
        print(f'Sending chunk {i}')
        yield streaming_pb2.DataChunk(
            content=client_id,
            sequence_number=i
        )
        time.sleep(1)

def run():
    # server_ip = input("Enter the server IP address: ") # Get the server IP address from the user
    # client_id = input("Enter the client ID: ") # Get the client ID from the user
    server_ip = sys.argv[0]
    client_id = sys.argv[1]
    # Open a gRPC channel to the server
    with grpc.insecure_channel(f'{server_ip}:50051') as channel:
        stub = streaming_pb2_grpc.DataProcessingServiceStub(channel)
        
        # Send data stream and receive occasional responses
        response_iterator = stub.ProcessDataStream(generate_data_chunks(client_id))
        
        for response in response_iterator:
            print(f"Response: {response.message}, {response.processed_sequence}")
            print('---')

if __name__ == "__main__":
    run()
