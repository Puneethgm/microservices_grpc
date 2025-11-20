#!/usr/bin/env python3
"""
Pure gRPC Client for testing microservices
"""
import grpc
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import service_pb2
import service_pb2_grpc
import weather_pb2
import weather_pb2_grpc
import profile_pb2
import profile_pb2_grpc
import gateway_pb2
import gateway_pb2_grpc


def test_hello_service(name="puneeth"):
    """Test Hello Service via gRPC"""
    print(f"\n🔹 Testing Hello Service: {name}")
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = service_pb2_grpc.HelloServiceStub(channel)
            request = service_pb2.HelloRequest(name=name)
            response = stub.SayHello(request, timeout=5)
            print(f"✅ Response: {response.message}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_weather_service(city="London", country=""):
    """Test Weather Service via gRPC"""
    print(f"\n🔹 Testing Weather Service: {city}")
    try:
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = weather_pb2_grpc.WeatherServiceStub(channel)
            request = weather_pb2.WeatherRequest(city=city, country_code=country)
            response = stub.GetWeather(request, timeout=15)
            
            if response.success:
                print(f"✅ Weather in {response.city}, {response.country}:")
                print(f"   🌡️  Temperature: {response.temperature_celsius}°C")
                print(f"   🌤️  Description: {response.description}")
                print(f"   💧 Humidity: {response.humidity}%")
                print(f"   💨 Wind Speed: {response.wind_speed:.1f} m/s")
            else:
                print(f"❌ Error: {response.error_message}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_profile_service(user_id="puneeth"):
    """Test Profile Service via gRPC"""
    print(f"\n🔹 Testing Profile Service: {user_id}")
    try:
        with grpc.insecure_channel('localhost:50053') as channel:
            stub = profile_pb2_grpc.ProfileServiceStub(channel)
            request = profile_pb2.ProfileRequest(user_id=user_id)
            response = stub.GetProfile(request, timeout=5)
            
            if response.success:
                print(f"✅ User Profile:")
                print(f"   👤 Name: {response.name}")
                print(f"   🏙️  Preferred City: {response.preferred_city}")
                print(f"   🌍 Country: {response.preferred_country}")
            else:
                print(f"❌ Error: {response.error_message}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_gateway_dashboard(user_id="puneeth"):
    """Test Gateway Dashboard via gRPC"""
    print(f"\n🔹 Testing Gateway Dashboard: {user_id}")
    try:
        with grpc.insecure_channel('localhost:50054') as channel:
            stub = gateway_pb2_grpc.GatewayServiceStub(channel)
            request = gateway_pb2.DashboardRequest(user_id=user_id)
            response = stub.GetDashboard(request, timeout=20)
            
            if response.success:
                print(f"✅ Complete Dashboard:")
                print(f"   💬 Greeting: {response.greeting}")
                print(f"   👤 User: {response.user_info.name} from {response.user_info.preferred_city}")
                print(f"   🌡️  Weather: {response.weather_info.temperature_celsius}°C, {response.weather_info.description}")
                print(f"   🌍 Location: {response.weather_info.city}, {response.weather_info.country}")
            else:
                print(f"❌ Error: {response.error_message}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_gateway_user_weather(user_id="puneeth"):
    """Test Gateway User Weather via gRPC"""
    print(f"\n🔹 Testing Gateway User Weather: {user_id}")
    try:
        with grpc.insecure_channel('localhost:50054') as channel:
            stub = gateway_pb2_grpc.GatewayServiceStub(channel)
            request = gateway_pb2.UserWeatherRequest(user_id=user_id)
            response = stub.GetUserWeather(request, timeout=20)
            
            if response.success:
                print(f"✅ User Weather:")
                print(f"   👤 User: {response.user_id}")
                print(f"   🏙️  City: {response.city}")
                print(f"   🌡️  Temperature: {response.weather_info.temperature_celsius}°C")
                print(f"   🌤️  Condition: {response.weather_info.description}")
            else:
                print(f"❌ Error: {response.error_message}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("🧪 Pure gRPC Microservices Testing")
    print("=" * 50)
    
    # Test individual services
    test_hello_service("puneeth")
    test_weather_service("Mumbai", "IN")
    test_profile_service("puneeth")
    test_profile_service("mohan")
    
    print("\n" + "=" * 50)
    print("🚀 Testing Gateway Service (Service Orchestration)")
    
    # Test gateway services
    test_gateway_dashboard("puneeth")
    test_gateway_user_weather("mohan")
    
    print("\n✨ Testing complete!")


if __name__ == "__main__":
    main()