import grpc
from concurrent import futures
import time
import streaming_pb2
import streaming_pb2_grpc

# Implement the service defined in the proto file
class DataProcessingServiceServicer(streaming_pb2_grpc.DataProcessingServiceServicer):

    def ProcessDataStream(self, request_iterator, context):
        for i, data_chunk in enumerate(request_iterator):
            # Simulate processing the incoming data chunk
            print(f"Received {data_chunk.content}, seq: {data_chunk.sequence_number}")
            yield streaming_pb2.ServerResponse(
                    message=f"Processed {data_chunk.content}",
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
