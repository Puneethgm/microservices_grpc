from concurrent import futures
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import service_pb2
import service_pb2_grpc


class HelloServicer(service_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        name = request.name or "world"
        print(f"[HelloService] Received request for: {name}")
        return service_pb2.HelloReply(message=f"Hello, {name} (from pure gRPC server)")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_HelloServiceServicer_to_server(HelloServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🚀 Hello gRPC Server started on port 50051")
    print("Press Ctrl+C to stop...")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped.")
        server.stop(0)


if __name__ == '__main__':
    serve()