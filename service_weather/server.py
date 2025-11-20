from concurrent import futures
import grpc
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import weather_pb2
import weather_pb2_grpc


class WeatherServicer(weather_pb2_grpc.WeatherServiceServicer):
    def GetWeather(self, request, context):
        city = request.city
        country_code = request.country_code or ""
        
        print(f"[WeatherService] Getting weather for: {city}, {country_code}")
        
        try:
            if not city:
                return weather_pb2.WeatherReply(
                    success=False,
                    error_message="City name is required"
                )
            
            query = f"{city},{country_code}" if country_code else city
            url = f"http://wttr.in/{query}?format=j1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                area = data['nearest_area'][0]
                
                result = weather_pb2.WeatherReply(
                    city=city.title(),
                    country=area.get('country', [{'value': 'Unknown'}])[0]['value'],
                    temperature_celsius=float(current['temp_C']),
                    description=current['weatherDesc'][0]['value'],
                    humidity=float(current['humidity']),
                    wind_speed=float(current['windspeedKmph']) * 0.277778,  # Convert to m/s
                    success=True,
                    error_message=""
                )
                
                print(f"[WeatherService] ✅ Success: {current['temp_C']}°C, {current['weatherDesc'][0]['value']}")
                return result
            else:
                error_msg = f"Weather API returned status {response.status_code}"
                print(f"[WeatherService] ❌ Error: {error_msg}")
                return weather_pb2.WeatherReply(
                    success=False,
                    error_message=error_msg
                )
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            print(f"[WeatherService] ❌ Network error: {error_msg}")
            return weather_pb2.WeatherReply(
                success=False,
                error_message=error_msg
            )
        except Exception as e:
            error_msg = f"Service error: {str(e)}"
            print(f"[WeatherService] ❌ Exception: {error_msg}")
            return weather_pb2.WeatherReply(
                success=False,
                error_message=error_msg
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("🌤️  Weather gRPC Server started on port 50052")
    print("Press Ctrl+C to stop...")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped.")
        server.stop(0)


if __name__ == '__main__':
    serve()