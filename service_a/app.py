"""
Pure gRPC Client Example - Service A
This demonstrates a simple gRPC client that calls the Hello Service
"""
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import service_pb2
import service_pb2_grpc


def call_hello_service(name):
    """Call the Hello Service via gRPC"""
    print(f"[ServiceA] Calling Hello Service for: {name}")
    
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = service_pb2_grpc.HelloServiceStub(channel)
            request = service_pb2.HelloRequest(name=name)
            response = stub.SayHello(request, timeout=5)
            
            print(f"[ServiceA] ✅ Response: {response.message}")
            return response.message
            
    except Exception as e:
        error_msg = f"Error calling Hello Service: {str(e)}"
        print(f"[ServiceA] ❌ {error_msg}")
        return error_msg


def main():
    """Main function - demonstrates gRPC client calls"""
    print("🔗 Service A - Pure gRPC Client")
    print("=" * 40)
    
    # Test multiple names
    test_names = ["Alice", "Bob", "Charlie", "puneeth", "mohan"]
    
    for name in test_names:
        call_hello_service(name)
        print()
    
    print("✨ Service A testing complete!")


if __name__ == '__main__':
    main()