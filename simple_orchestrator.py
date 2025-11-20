#!/usr/bin/env python3
"""
Simple CLI Commands for Multi-Microservice Orchestration
Fixed encoding issues for Windows PowerShell
"""
import grpc
import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all gRPC modules
import service_pb2, service_pb2_grpc
import weather_pb2, weather_pb2_grpc
import profile_pb2, profile_pb2_grpc
import gateway_pb2, gateway_pb2_grpc


class SimpleOrchestrator:
    """Simple orchestrator without Unicode characters for Windows compatibility"""
    
    def __init__(self):
        self.services = {
            'hello': 'localhost:50051',
            'weather': 'localhost:50052', 
            'profile': 'localhost:50053',
            'gateway': 'localhost:50054'
        }
    
    def get_user_dashboard(self, user_id):
        """Get complete user dashboard from all microservices"""
        print(f"Connecting ALL microservices for user: {user_id}")
        
        try:
            with grpc.insecure_channel(self.services['gateway']) as channel:
                stub = gateway_pb2_grpc.GatewayServiceStub(channel)
                request = gateway_pb2.DashboardRequest(user_id=user_id)
                response = stub.GetDashboard(request, timeout=20)
                
                if response.success:
                    return {
                        "status": "SUCCESS",
                        "timestamp": datetime.now().isoformat(),
                        "user_info": {
                            "user_id": response.user_info.user_id,
                            "name": response.user_info.name,
                            "location": f"{response.user_info.preferred_city}, {response.user_info.preferred_country}"
                        },
                        "greeting": response.greeting,
                        "weather": {
                            "location": f"{response.weather_info.city}, {response.weather_info.country}",
                            "temperature_celsius": response.weather_info.temperature_celsius,
                            "condition": response.weather_info.description,
                            "humidity_percent": response.weather_info.humidity,
                            "wind_speed_ms": round(response.weather_info.wind_speed, 1)
                        },
                        "services_used": ["Gateway", "Profile", "Weather", "Hello"],
                        "architecture": "Pure gRPC Microservices"
                    }
                else:
                    return {"status": "FAILED", "error": response.error_message}
                    
        except Exception as e:
            return {"status": "CONNECTION_FAILED", "error": str(e)}
    
    def compare_users(self, user_list):
        """Compare multiple users"""
        print(f"Multi-user comparison: {', '.join(user_list)}")
        
        results = []
        for user_id in user_list:
            result = self.get_user_dashboard(user_id)
            if result.get("status") == "SUCCESS":
                results.append({
                    "user": user_id,
                    "name": result["user_info"]["name"],
                    "location": result["user_info"]["location"],
                    "temperature": result["weather"]["temperature_celsius"],
                    "condition": result["weather"]["condition"]
                })
        
        return {
            "status": "MULTI_USER_SUCCESS",
            "comparison_data": results,
            "users_processed": len(results),
            "microservices_used": ["Gateway", "Profile", "Weather", "Hello"]
        }
    
    def aggregate_weather(self, cities):
        """Get weather from multiple cities"""
        print(f"Weather aggregation: {', '.join(cities)}")
        
        weather_data = []
        
        with grpc.insecure_channel(self.services['weather']) as channel:
            stub = weather_pb2_grpc.WeatherServiceStub(channel)
            
            for city in cities:
                try:
                    request = weather_pb2.WeatherRequest(city=city)
                    response = stub.GetWeather(request, timeout=10)
                    
                    if response.success:
                        weather_data.append({
                            "city": response.city,
                            "country": response.country,
                            "temperature": response.temperature_celsius,
                            "condition": response.description,
                            "humidity": response.humidity
                        })
                except Exception as e:
                    weather_data.append({"city": city, "error": str(e)})
        
        # Calculate stats
        temps = [w["temperature"] for w in weather_data if "temperature" in w]
        
        return {
            "status": "WEATHER_SUCCESS",
            "cities_data": weather_data,
            "statistics": {
                "cities_processed": len(weather_data),
                "average_temperature": round(sum(temps) / len(temps), 1) if temps else 0,
                "hottest_city": max(weather_data, key=lambda x: x.get("temperature", -999))["city"] if temps else None,
                "coldest_city": min(weather_data, key=lambda x: x.get("temperature", 999))["city"] if temps else None
            }
        }


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python simple_orchestrator.py dashboard <user_id>")
        print("  python simple_orchestrator.py compare <user1> <user2> [user3...]")
        print("  python simple_orchestrator.py weather <city1> <city2> [city3...]")
        return
    
    orchestrator = SimpleOrchestrator()
    command = sys.argv[1].lower()
    
    if command == "dashboard":
        if len(sys.argv) < 3:
            print("Error: Please provide user_id")
            return
        user_id = sys.argv[2]
        result = orchestrator.get_user_dashboard(user_id)
        print(json.dumps(result, indent=2))
        
    elif command == "compare":
        if len(sys.argv) < 4:
            print("Error: Please provide at least 2 user_ids")
            return
        users = sys.argv[2:]
        result = orchestrator.compare_users(users)
        print(json.dumps(result, indent=2))
        
    elif command == "weather":
        if len(sys.argv) < 4:
            print("Error: Please provide at least 2 cities")
            return
        cities = sys.argv[2:]
        result = orchestrator.aggregate_weather(cities)
        print(json.dumps(result, indent=2))
        
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()