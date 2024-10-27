import grpc
import streaming_pb2
import streaming_pb2_grpc
import time
import sys
from concurrent.futures import ThreadPoolExecutor

def generate_data_chunks(client_id):
    # Simulate sending a stream of data
    for i in range(1, 21):  # Send 20 chunks of data
        print(f'Sending chunk {i}')
        yield streaming_pb2.DataChunk(
            content=client_id,
            sequence_number=i
        )
        time.sleep(1)

def run_client(server_ip, client_id):
    # Open a gRPC channel to the server
    with grpc.insecure_channel(f'{server_ip}:50051') as channel:
        stub = streaming_pb2_grpc.DataProcessingServiceStub(channel)
        
        # Send data stream and receive occasional responses
        response_iterator = stub.ProcessDataStream(generate_data_chunks(client_id))
        
        for response in response_iterator:
            print(f"Client {client_id} Response: {response.message}, {response.processed_sequence}")
            print('---')

def main():
    server_ip = sys.argv[1]  # Get the server IP address from command-line arguments
    num_clients = int(sys.argv[2])  # Number of clients to start

    # Use ThreadPoolExecutor to manage multiple client threads
    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        futures = []
        for i in range(num_clients):
            client_id = f"client_{i + 1}"
            futures.append(executor.submit(run_client, server_ip, client_id))

        # Wait for all threads to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
