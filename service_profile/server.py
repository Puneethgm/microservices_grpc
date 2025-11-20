import threading
from concurrent import futures
import grpc
from flask import Flask, jsonify, request
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import profile_pb2
import profile_pb2_grpc
import weather_pb2
import weather_pb2_grpc

# Simple in-memory user storage:
USERS_DB = {
    "puneeth": {"name": "Puneeth G M", "preferred_city": "Bengaluru", "preferred_country": "IN"},
    "alice": {"name": "Ravi", "preferred_city": "Bengaluru", "preferred_country": "IN"},
    "bob": {"name": "Summit", "preferred_city": "New York", "preferred_country": "US"},
    "charlie": {"name": "Mohan", "preferred_city": "Tokyo", "preferred_country": "JP"}
}


class ProfileServicer(profile_pb2_grpc.ProfileServiceServicer):
    def GetProfile(self, request, context):
        user_id = request.user_id.lower()
        
        if user_id not in USERS_DB:
            return profile_pb2.ProfileReply(
                success=False,
                error_message=f"User '{request.user_id}' not found"
            )
        
        user_data = USERS_DB[user_id]
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


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profile_pb2_grpc.add_ProfileServiceServicer_to_server(ProfileServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Profile gRPC server started on port 50053")
    server.wait_for_termination()


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        "service": "profile_service",
        "status": "ok",
        "users": list(USERS_DB.keys())
    })


@app.route('/profile/<user_id>')
def get_profile_http(user_id):
    try:
        with grpc.insecure_channel('localhost:50053') as channel:
            stub = profile_pb2_grpc.ProfileServiceStub(channel)
            request = profile_pb2.ProfileRequest(user_id=user_id)
            response = stub.GetProfile(request, timeout=5)
            
            return jsonify({
                "user_id": response.user_id,
                "name": response.name,
                "preferred_city": response.preferred_city,
                "preferred_country": response.preferred_country,
                "success": response.success,
                "error": response.error_message if not response.success else None
            })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


@app.route('/profile/<user_id>/weather')
def get_user_weather_http(user_id):
    try:
        with grpc.insecure_channel('localhost:50053') as channel:
            stub = profile_pb2_grpc.ProfileServiceStub(channel)
            profile_req = profile_pb2.ProfileRequest(user_id=user_id)
            profile_resp = stub.GetProfile(profile_req, timeout=5)
            
            if not profile_resp.success:
                return jsonify({"error": profile_resp.error_message, "success": False}), 404
        
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = weather_pb2_grpc.WeatherServiceStub(channel)
            weather_req = weather_pb2.WeatherRequest(
                city=profile_resp.preferred_city,
                country_code=profile_resp.preferred_country
            )
            weather_resp = stub.GetWeather(weather_req, timeout=15)
            
            return jsonify({
                "user": {
                    "user_id": profile_resp.user_id,
                    "name": profile_resp.name,
                    "preferred_city": profile_resp.preferred_city
                },
                "weather": {
                    "city": weather_resp.city,
                    "country": weather_resp.country,
                    "temperature_celsius": weather_resp.temperature_celsius,
                    "description": weather_resp.description,
                    "humidity": weather_resp.humidity,
                    "wind_speed_ms": weather_resp.wind_speed,
                    "success": weather_resp.success,
                    "error": weather_resp.error_message if not weather_resp.success else None
                }
            })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


if __name__ == '__main__':
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    grpc_thread.start()
    
    print("Profile service starting...")
    print("gRPC server: localhost:50053")
    print("HTTP server: localhost:5004")
    
    app.run(host='0.0.0.0', port=5004)