from concurrent import futures
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
import gateway_pb2
import gateway_pb2_grpc


class GatewayServicer(gateway_pb2_grpc.GatewayServiceServicer):
    def GetDashboard(self, request, context):
        user_id = request.user_id
        
        print(f"[GatewayService] Building dashboard for: {user_id}")
        
        try:
            # Get greeting from Hello service
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = service_pb2_grpc.HelloServiceStub(channel)
                hello_req = service_pb2.HelloRequest(name=user_id)
                hello_resp = stub.SayHello(hello_req, timeout=5)
                greeting = hello_resp.message
            
            # Get user profile
            with grpc.insecure_channel('localhost:50053') as channel:
                stub = profile_pb2_grpc.ProfileServiceStub(channel)
                profile_req = profile_pb2.ProfileRequest(user_id=user_id)
                profile_resp = stub.GetProfile(profile_req, timeout=5)
                
                if not profile_resp.success:
                    return gateway_pb2.DashboardReply(
                        success=False,
                        error_message=profile_resp.error_message
                    )
            
            # Get weather for user's preferred city
            with grpc.insecure_channel('localhost:50052') as channel:
                stub = weather_pb2_grpc.WeatherServiceStub(channel)
                weather_req = weather_pb2.WeatherRequest(
                    city=profile_resp.preferred_city,
                    country_code=profile_resp.preferred_country
                )
                weather_resp = stub.GetWeather(weather_req, timeout=15)
            
            # Build response
            user_info = gateway_pb2.UserInfo(
                user_id=profile_resp.user_id,
                name=profile_resp.name,
                preferred_city=profile_resp.preferred_city,
                preferred_country=profile_resp.preferred_country
            )
            
            weather_info = gateway_pb2.WeatherInfo(
                city=weather_resp.city,
                country=weather_resp.country,
                temperature_celsius=weather_resp.temperature_celsius,
                description=weather_resp.description,
                humidity=weather_resp.humidity,
                wind_speed=weather_resp.wind_speed
            )
            
            print(f"[GatewayService] ✅ Dashboard complete for {user_id}")
            
            return gateway_pb2.DashboardReply(
                greeting=greeting,
                user_info=user_info,
                weather_info=weather_info,
                success=True,
                error_message=""
            )
            
        except Exception as e:
            print(f"[GatewayService] ❌ Error building dashboard: {str(e)}")
            return gateway_pb2.DashboardReply(
                success=False,
                error_message=f"Dashboard error: {str(e)}"
            )
    
    def GetUserWeather(self, request, context):
        user_id = request.user_id
        
        print(f"[GatewayService] Getting weather for user: {user_id}")
        
        try:
            # Get user profile first
            with grpc.insecure_channel('localhost:50053') as channel:
                stub = profile_pb2_grpc.ProfileServiceStub(channel)
                profile_req = profile_pb2.ProfileRequest(user_id=user_id)
                profile_resp = stub.GetProfile(profile_req, timeout=5)
                
                if not profile_resp.success:
                    return gateway_pb2.UserWeatherReply(
                        success=False,
                        error_message=profile_resp.error_message
                    )
            
            # Get weather for user's preferred city
            with grpc.insecure_channel('localhost:50052') as channel:
                stub = weather_pb2_grpc.WeatherServiceStub(channel)
                weather_req = weather_pb2.WeatherRequest(
                    city=profile_resp.preferred_city,
                    country_code=profile_resp.preferred_country
                )
                weather_resp = stub.GetWeather(weather_req, timeout=15)
            
            weather_info = gateway_pb2.WeatherInfo(
                city=weather_resp.city,
                country=weather_resp.country,
                temperature_celsius=weather_resp.temperature_celsius,
                description=weather_resp.description,
                humidity=weather_resp.humidity,
                wind_speed=weather_resp.wind_speed
            )
            
            print(f"[GatewayService] ✅ User weather complete for {user_id}")
            
            return gateway_pb2.UserWeatherReply(
                user_id=user_id,
                city=profile_resp.preferred_city,
                weather_info=weather_info,
                success=True,
                error_message=""
            )
            
        except Exception as e:
            print(f"[GatewayService] ❌ Error getting user weather: {str(e)}")
            return gateway_pb2.UserWeatherReply(
                success=False,
                error_message=f"User weather error: {str(e)}"
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gateway_pb2_grpc.add_GatewayServiceServicer_to_server(GatewayServicer(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("🚀 Gateway gRPC Server started on port 50054")
    print("Available services:")
    print("  - GetDashboard: Complete user dashboard")
    print("  - GetUserWeather: User's weather info")
    print("Press Ctrl+C to stop...")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped.")
        server.stop(0)


if __name__ == '__main__':
    serve()