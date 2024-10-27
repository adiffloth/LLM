import grpc
from concurrent import futures
import streaming_pb2
import streaming_pb2_grpc
import threading

# Implement the service defined in the proto file
class DataProcessingServiceServicer(streaming_pb2_grpc.DataProcessingServiceServicer):

    def __init__(self):
        self.lock = threading.Lock()
        self.counter = 0

    def ProcessDataStream(self, request_iterator, context):
        for data_chunk in request_iterator:
            with self.lock:
                self.counter += 1
                current_counter = self.counter

            # Simulate processing the incoming data chunk
            print(f"{self.counter} Received seq {data_chunk.sequence_number} from client {data_chunk.content}")
            yield streaming_pb2.ServerResponse(
                    message=f"Processed {data_chunk.content}-{data_chunk.sequence_number}",
                    processed_sequence=data_chunk.sequence_number
                )


# Start the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_DataProcessingServiceServicer_to_server(DataProcessingServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
