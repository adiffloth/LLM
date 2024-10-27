import grpc
import streaming_pb2
import streaming_pb2_grpc
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread

def generate_data_chunks(client_id, thread_id, num_chunks):
    # Simulate sending a stream of data
    for i in range(1, num_chunks+1):  # Send 20 chunks of data
        # print(f'Client {client_id} thread {thread_id} sending chunk {i}')
        print(f'send {client_id}-{thread_id}-{i}')
        yield streaming_pb2.DataChunk(
            content=f'{client_id}-{thread_id}',
            sequence_number=i
        )
        time.sleep(1)

def run_client(server_ip, client_id, num_chunks):
    thread_id = current_thread().name.split('-')[-1]  # Get the thread ID
    # Open a gRPC channel to the server
    with grpc.insecure_channel(f'{server_ip}:50051') as channel:
        stub = streaming_pb2_grpc.DataProcessingServiceStub(channel)
        
        # Send data stream and receive occasional responses
        response_iterator = stub.ProcessDataStream(generate_data_chunks(client_id, thread_id, num_chunks))
        
        for response in response_iterator:
            print(f"recv {response.message}, {response.processed_sequence}")
            print('---')

def main():
    server_ip = sys.argv[1]  # Get the server IP address from command-line arguments
    client_id = sys.argv[2]  # Get the client ID from command-line arguments
    num_threads = int(sys.argv[3])  # Number of threads to start
    num_chunks = int(sys.argv[4])  # Number of chunks to send per client

    # Use ThreadPoolExecutor to manage multiple client threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_threads):
            futures.append(executor.submit(run_client, server_ip, client_id, num_chunks))
            time.sleep(1/num_threads)

        # Wait for all threads to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
