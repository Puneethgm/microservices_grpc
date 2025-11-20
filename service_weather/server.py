import threading
from concurrent import futures
import grpc
from flask import Flask, jsonify, request
import sys
import os
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import weather_pb2
import weather_pb2_grpc

class WeatherServicer(weather_pb2_grpc.WeatherServiceServicer):
    def GetWeather(self, request, context):
        try:
            city = request.city
            if not city:
                return weather_pb2.WeatherReply(
                    success=False,
                    error_message="City name is required"
                )
            
            url = f"http://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return weather_pb2.WeatherReply(
                    success=False,
                    error_message=f"Weather API returned status {response.status_code}"
                )
            
            data = response.json()
            current = data['current_condition'][0]
            area = data['nearest_area'][0]
            
            return weather_pb2.WeatherReply(
                city=city.title(),
                country=area.get('country', [{'value': 'Unknown'}])[0]['value'],
                temperature_celsius=float(current['temp_C']),
                description=current['weatherDesc'][0]['value'],
                humidity=float(current['humidity']),
                wind_speed=float(current['windspeedKmph']) * 0.277778,
                success=True,
                error_message=""
            )
            
        except requests.exceptions.RequestException as e:
            return weather_pb2.WeatherReply(
                success=False,
                error_message=f"Network error: {str(e)}"
            )
        except Exception as e:
            return weather_pb2.WeatherReply(
                success=False,
                error_message=f"Service error: {str(e)}"
            )


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Weather gRPC server started on port 50052")
    server.wait_for_termination()


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        "service": "weather_service",
        "status": "ok",
        "description": "Weather microservice using wttr.in API"
    })


@app.route('/weather/<city>')
def get_weather_http(city):
    try:
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = weather_pb2_grpc.WeatherServiceStub(channel)
            request = weather_pb2.WeatherRequest(city=city)
            response = stub.GetWeather(request, timeout=15)
            
            return jsonify({
                "city": response.city,
                "country": response.country,
                "temperature_celsius": response.temperature_celsius,
                "description": response.description,
                "humidity": response.humidity,
                "wind_speed_ms": response.wind_speed,
                "success": response.success,
                "error": response.error_message if not response.success else None
            })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


if __name__ == '__main__':
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    grpc_thread.start()
    
    print("Weather service starting...")
    print("gRPC server: localhost:50052")
    print("HTTP server: localhost:5003")
    
    app.run(host='0.0.0.0', port=5003)