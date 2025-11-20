from flask import Flask, jsonify, request
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import service_pb2
import service_pb2_grpc
import weather_pb2
import weather_pb2_grpc
import profile_pb2
import profile_pb2_grpc

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        "service": "api_gateway",
        "status": "ok",
        "description": "API Gateway orchestrating multiple microservices",
        "endpoints": {
            "/hello/<name>": "Simple greeting via Service A",
            "/weather/<city>": "Get weather for any city",
            "/user/<user_id>": "Get user profile",
            "/user/<user_id>/weather": "Get weather for user's preferred city",
            "/dashboard/<user_id>": "Full dashboard with user info and weather"
        }
    })


@app.route('/hello/<name>')
def hello_service(name):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = service_pb2_grpc.HelloServiceStub(channel)
            req = service_pb2.HelloRequest(name=name)
            res = stub.SayHello(req, timeout=5)
            return jsonify({"message": res.message, "source": "hello_service"})
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


@app.route('/weather/<city>')
def weather_service(city):
    try:
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = weather_pb2_grpc.WeatherServiceStub(channel)
            req = weather_pb2.WeatherRequest(city=city)
            res = stub.GetWeather(req, timeout=15)
            
            if not res.success:
                return jsonify({"error": res.error_message, "success": False}), 400
                
            return jsonify({
                "city": res.city,
                "country": res.country,
                "temperature_celsius": res.temperature_celsius,
                "temperature_fahrenheit": round(res.temperature_celsius * 9/5 + 32, 1),
                "description": res.description,
                "humidity": res.humidity,
                "wind_speed_ms": res.wind_speed,
                "source": "weather_service"
            })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


@app.route('/user/<user_id>')
def user_profile(user_id):
    try:
        with grpc.insecure_channel('localhost:50053') as channel:
            stub = profile_pb2_grpc.ProfileServiceStub(channel)
            req = profile_pb2.ProfileRequest(user_id=user_id)
            res = stub.GetProfile(req, timeout=5)
            
            if not res.success:
                return jsonify({"error": res.error_message, "success": False}), 404
                
            return jsonify({
                "user_id": res.user_id,
                "name": res.name,
                "preferred_city": res.preferred_city,
                "preferred_country": res.preferred_country,
                "source": "profile_service"
            })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


@app.route('/user/<user_id>/weather')
def user_weather(user_id):
    try:
        # Get user profile
        with grpc.insecure_channel('localhost:50053') as channel:
            stub = profile_pb2_grpc.ProfileServiceStub(channel)
            profile_req = profile_pb2.ProfileRequest(user_id=user_id)
            profile_res = stub.GetProfile(profile_req, timeout=5)
            
            if not profile_res.success:
                return jsonify({"error": profile_res.error_message, "success": False}), 404
        
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = weather_pb2_grpc.WeatherServiceStub(channel)
            weather_req = weather_pb2.WeatherRequest(
                city=profile_res.preferred_city,
                country_code=profile_res.preferred_country
            )
            weather_res = stub.GetWeather(weather_req, timeout=15)
            
            return jsonify({
                "user": {
                    "user_id": profile_res.user_id,
                    "name": profile_res.name
                },
                "weather": {
                    "city": weather_res.city,
                    "country": weather_res.country,
                    "temperature_celsius": weather_res.temperature_celsius,
                    "temperature_fahrenheit": round(weather_res.temperature_celsius * 9/5 + 32, 1),
                    "description": weather_res.description,
                    "humidity": weather_res.humidity,
                    "wind_speed_ms": weather_res.wind_speed,
                    "success": weather_res.success,
                    "error": weather_res.error_message if not weather_res.success else None
                },
                "sources": ["profile_service", "weather_service"]
            })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


@app.route('/dashboard/<user_id>')
def user_dashboard(user_id):
    try:
        # Get user profile
        with grpc.insecure_channel('localhost:50053') as channel:
            stub = profile_pb2_grpc.ProfileServiceStub(channel)
            profile_req = profile_pb2.ProfileRequest(user_id=user_id)
            profile_res = stub.GetProfile(profile_req, timeout=5)
            
            if not profile_res.success:
                return jsonify({"error": profile_res.error_message, "success": False}), 404
        
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = service_pb2_grpc.HelloServiceStub(channel)
            hello_req = service_pb2.HelloRequest(name=profile_res.name)
            hello_res = stub.SayHello(hello_req, timeout=5)
        
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = weather_pb2_grpc.WeatherServiceStub(channel)
            weather_req = weather_pb2.WeatherRequest(
                city=profile_res.preferred_city,
                country_code=profile_res.preferred_country
            )
            weather_res = stub.GetWeather(weather_req, timeout=15)
            
            return jsonify({
                "greeting": hello_res.message,
                "profile": {
                    "user_id": profile_res.user_id,
                    "name": profile_res.name,
                    "preferred_city": profile_res.preferred_city,
                    "preferred_country": profile_res.preferred_country
                },
                "weather": {
                    "city": weather_res.city,
                    "country": weather_res.country,
                    "temperature_celsius": weather_res.temperature_celsius,
                    "temperature_fahrenheit": round(weather_res.temperature_celsius * 9/5 + 32, 1),
                    "description": weather_res.description,
                    "humidity": weather_res.humidity,
                    "wind_speed_ms": weather_res.wind_speed,
                    "success": weather_res.success,
                    "error": weather_res.error_message if not weather_res.success else None
                },
                "services_called": ["hello_service", "profile_service", "weather_service"]
            })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


if __name__ == '__main__':
    print("API Gateway starting...")
    print("Endpoints available:")
    print("  - http://localhost:5000/")
    print("  - http://localhost:5000/hello/<name>")  
    print("  - http://localhost:5000/weather/<city>")
    print("  - http://localhost:5000/user/<user_id>")
    print("  - http://localhost:5000/user/<user_id>/weather")
    print("  - http://localhost:5000/dashboard/<user_id>")
    
    app.run(host='0.0.0.0', port=5000)