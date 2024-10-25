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
            print(f"Received chunk {data_chunk.sequence_number}: {data_chunk.content}")
            
            # Occasionally send a response back to the client
            if data_chunk.sequence_number % 3 == 0:  # Respond every 5 messages
                yield streaming_pb2.ServerResponse(
                    message=f"Processed 3 chunks {data_chunk.sequence_number}",
                    processed_sequence=data_chunk.sequence_number
                )
            if data_chunk.sequence_number % 5 == 0:  # Respond every 5 messages
                yield streaming_pb2.ServerResponse(
                    message=f"Processed 5 chunks {data_chunk.sequence_number}",
                    processed_sequence=data_chunk.sequence_number
                )
                # time.sleep(0.1)  # Simulate some processing time

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
