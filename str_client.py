import grpc
import streaming_pb2
import streaming_pb2_grpc
import time

def generate_data_chunks():
    # Simulate sending a stream of data
    for i in range(1, 21):  # Send 20 chunks of data
        print(f'Sending chunk {i}')
        yield streaming_pb2.DataChunk(
            content=f"This is chunk {i}",
            sequence_number=i
        )
        time.sleep(0.1)

def run():
    # Open a gRPC channel to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = streaming_pb2_grpc.DataProcessingServiceStub(channel)
        
        # Send data stream and receive occasional responses
        response_iterator = stub.ProcessDataStream(generate_data_chunks())
        
        for response in response_iterator:
            print(f"Received response from server: {response.message}, processed sequence: {response.processed_sequence}")

if __name__ == "__main__":
    run()
