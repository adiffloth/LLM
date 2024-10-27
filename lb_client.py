import grpc
import streaming_pb2
import streaming_pb2_grpc
import time

def generate_data_chunks(client_id):
    # Simulate sending a stream of data
    for i in range(1, 21):  # Send 20 chunks of data
        msg = f'{client_id} - {i}'
        print(f'Sending chunk {msg}')
        yield streaming_pb2.DataChunk(
            content=msg,
            sequence_number=i
        )
        time.sleep(1)

def run():
    server_ip = input("Enter the server IP address: ") # Get the server IP address from the user
    client_id = input("Enter the client ID: ") # Get the client ID from the user
    # Open a gRPC channel to the server
    with grpc.insecure_channel(f'{server_ip}:50051') as channel:
        stub = streaming_pb2_grpc.DataProcessingServiceStub(channel)
        
        # Send data stream and receive occasional responses
        response_iterator = stub.ProcessDataStream(generate_data_chunks(client_id))
        
        for response in response_iterator:
            print(f"Response: {response.message}, {response.processed_sequence}")

if __name__ == "__main__":
    run()
