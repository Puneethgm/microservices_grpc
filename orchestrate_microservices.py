#!/usr/bin/env python3
"""
Multi-Microservice Orchestration Client
This demonstrates connecting multiple microservices to get a single unified output
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


class MicroserviceOrchestrator:
    """Orchestrates multiple microservices to provide unified responses"""
    
    def __init__(self):
        self.services = {
            'hello': 'localhost:50051',
            'weather': 'localhost:50052', 
            'profile': 'localhost:50053',
            'gateway': 'localhost:50054'
        }
    
    def get_complete_user_dashboard(self, user_id):
        """
        🎯 COMMAND: Connect ALL microservices for complete user dashboard
        This calls: Gateway -> Profile -> Weather -> Hello services
        """
        print(f"🔗 Orchestrating ALL microservices for user: {user_id}")
        
        try:
            with grpc.insecure_channel(self.services['gateway']) as channel:
                stub = gateway_pb2_grpc.GatewayServiceStub(channel)
                request = gateway_pb2.DashboardRequest(user_id=user_id)
                response = stub.GetDashboard(request, timeout=20)
                
                if response.success:
                    return {
                        "🎯 unified_output": "SUCCESS",
                        "🕒 timestamp": datetime.now().isoformat(),
                        "👤 user_info": {
                            "user_id": response.user_info.user_id,
                            "name": response.user_info.name,
                            "location": f"{response.user_info.preferred_city}, {response.user_info.preferred_country}"
                        },
                        "💬 greeting": response.greeting,
                        "🌤️ weather": {
                            "location": f"{response.weather_info.city}, {response.weather_info.country}",
                            "temperature": f"{response.weather_info.temperature_celsius}°C",
                            "condition": response.weather_info.description,
                            "humidity": f"{response.weather_info.humidity}%",
                            "wind_speed": f"{response.weather_info.wind_speed:.1f} m/s"
                        },
                        "📊 services_called": ["Gateway", "Profile", "Weather", "Hello"],
                        "🏗️ architecture": "Pure gRPC Microservices"
                    }
                else:
                    return {"error": response.error_message, "unified_output": "FAILED"}
                    
        except Exception as e:
            return {"error": str(e), "unified_output": "CONNECTION_FAILED"}
    
    def get_multi_user_comparison(self, user_ids):
        """
        🎯 COMMAND: Compare multiple users across all services
        """
        print(f"🔗 Multi-user orchestration for: {', '.join(user_ids)}")
        
        results = []
        for user_id in user_ids:
            result = self.get_complete_user_dashboard(user_id)
            if "error" not in result:
                results.append({
                    "user": user_id,
                    "name": result["👤 user_info"]["name"],
                    "location": result["👤 user_info"]["location"],
                    "temperature": result["🌤️ weather"]["temperature"],
                    "condition": result["🌤️ weather"]["condition"]
                })
        
        return {
            "🎯 unified_output": "MULTI_USER_SUCCESS",
            "📊 comparison_data": results,
            "🔢 users_processed": len(results),
            "🏗️ microservices_used": ["Gateway", "Profile", "Weather", "Hello"]
        }
    
    def get_weather_aggregation(self, cities):
        """
        🎯 COMMAND: Aggregate weather from multiple cities
        """
        print(f"🔗 Weather aggregation for cities: {', '.join(cities)}")
        
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
        
        # Calculate aggregations
        temps = [w["temperature"] for w in weather_data if "temperature" in w]
        
        return {
            "🎯 unified_output": "WEATHER_AGGREGATION_SUCCESS",
            "🌍 cities_data": weather_data,
            "📊 aggregation": {
                "cities_processed": len(weather_data),
                "average_temperature": round(sum(temps) / len(temps), 1) if temps else 0,
                "hottest_city": max(weather_data, key=lambda x: x.get("temperature", -999))["city"] if temps else None,
                "coldest_city": min(weather_data, key=lambda x: x.get("temperature", 999))["city"] if temps else None
            }
        }


def main():
    """Main function with multiple orchestration examples"""
    orchestrator = MicroserviceOrchestrator()
    
    print("🚀 MULTI-MICROSERVICE ORCHESTRATION COMMANDS")
    print("=" * 60)
    
    # Command 1: Complete user dashboard (ALL services)
    print("\n🎯 COMMAND 1: Complete User Dashboard (4 Microservices)")
    print("-" * 50)
    result1 = orchestrator.get_complete_user_dashboard("puneeth")
    print(json.dumps(result1, indent=2))
    
    # Command 2: Multi-user comparison  
    print("\n🎯 COMMAND 2: Multi-User Comparison (Profile + Weather Services)")
    print("-" * 50)
    result2 = orchestrator.get_multi_user_comparison(["puneeth", "mohan", "john"])
    print(json.dumps(result2, indent=2))
    
    # Command 3: Weather aggregation
    print("\n🎯 COMMAND 3: Weather Aggregation (Weather Service)")
    print("-" * 50)
    result3 = orchestrator.get_weather_aggregation(["Mumbai", "Delhi", "Bengaluru", "Chennai", "London"])
    print(json.dumps(result3, indent=2))


if __name__ == "__main__":
    main()