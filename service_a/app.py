from flask import Flask, jsonify
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import service_pb2
import service_pb2_grpc

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"service": "service_a", "status": "ok"})


@app.route('/hello/<name>')
def hello(name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.HelloServiceStub(channel)
        req = service_pb2.HelloRequest(name=name)
        res = stub.SayHello(req, timeout=5)
        return jsonify({"message": res.message})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)