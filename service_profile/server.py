from concurrent import futures
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import profile_pb2
import profile_pb2_grpc

# Simple in-memory user storage:
USERS_DB = {
    "puneeth": {"name": "Puneeth G M", "preferred_city": "Bengaluru", "preferred_country": "IN"},
    "ravi": {"name": "Ravi", "preferred_city": "Bengaluru", "preferred_country": "IN"},
    "summit": {"name": "Summit", "preferred_city": "New York", "preferred_country": "US"},
    "mohan": {"name": "Mohan Kumar", "preferred_city": "Chennai", "preferred_country": "IN"},
    "john": {"name": "John Doe", "preferred_city": "London", "preferred_country": "GB"}
}


class ProfileServicer(profile_pb2_grpc.ProfileServiceServicer):
    def GetProfile(self, request, context):
        user_id = request.user_id.lower()
        
        print(f"[ProfileService] Getting profile for: {user_id}")
        
        if user_id not in USERS_DB:
            print(f"[ProfileService] ❌ User not found: {user_id}. Available: {list(USERS_DB.keys())}")
            return profile_pb2.ProfileReply(
                user_id=request.user_id,
                success=False,
                error_message=f"User '{request.user_id}' not found"
            )
        
        user_data = USERS_DB[user_id]
        print(f"[ProfileService] ✅ Found user: {user_data['name']} from {user_data['preferred_city']}")
        
        return profile_pb2.ProfileReply(
            user_id=request.user_id,
            name=user_data["name"],
            preferred_city=user_data["preferred_city"],
            preferred_country=user_data["preferred_country"],
            success=True,
            error_message=""
        )
    
    def UpdateCity(self, request, context):
        user_id = request.user_id.lower()
        
        print(f"[ProfileService] Updating city for {user_id}: {request.city}, {request.country_code}")
        
        if user_id not in USERS_DB:
            return profile_pb2.UpdateCityReply(
                success=False,
                message=f"User '{request.user_id}' not found"
            )
        
        USERS_DB[user_id]["preferred_city"] = request.city
        USERS_DB[user_id]["preferred_country"] = request.country_code
        
        return profile_pb2.UpdateCityReply(
            success=True,
            message=f"Updated {request.user_id}'s preferred city to {request.city}"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profile_pb2_grpc.add_ProfileServiceServicer_to_server(ProfileServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("👤 Profile gRPC Server started on port 50053")
    print(f"Available users: {list(USERS_DB.keys())}")
    print("Press Ctrl+C to stop...")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped.")
        server.stop(0)


if __name__ == '__main__':
    serve()