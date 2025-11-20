import threading
from concurrent import futures
import grpc
from flask import Flask, jsonify, request
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import service_pb2
import service_pb2_grpc


class HelloServicer(service_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        name = request.name or "world"
        return service_pb2.HelloReply(message=f"Hello, {name} (from gRPC server)")


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_HelloServiceServicer_to_server(HelloServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on 50051")
    server.wait_for_termination()


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"service": "service_b", "status": "ok"})


@app.route('/http-hello', methods=['GET'])
def http_hello():
    name = request.args.get('name', 'world')
    return jsonify({"message": f"Hello, {name} (from Flask HTTP in service B)"})


if __name__ == '__main__':
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    grpc_thread.start()
    app.run(host='0.0.0.0', port=5001)