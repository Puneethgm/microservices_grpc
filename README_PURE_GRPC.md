# Pure gRPC Microservices Architecture 🚀

## Overview

This project demonstrates a **pure gRPC microservices architecture** using Protocol Buffers for efficient inter-service communication. No HTTP/REST endpoints - everything communicates via gRPC protocol.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     gRPC Microservices                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Gateway   │────│  Profile    │────│  Weather    │        │
│  │ Service     │    │ Service     │    │ Service     │        │
│  │ :50054      │    │ :50053      │    │ :50052      │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│         │                                                      │
│         └─────────────────┬──────────────────────────────────  │
│                           │                                    │
│                    ┌─────────────┐    ┌─────────────┐        │
│                    │   Hello     │    │ Service A   │        │
│                    │ Service     │    │ (Client)    │        │
│                    │ :50051      │    │             │        │
│                    └─────────────┘    └─────────────┘        │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## Services

| Service             | Port  | Description                                                  |
| ------------------- | ----- | ------------------------------------------------------------ |
| **Gateway Service** | 50054 | Orchestrates all services, provides dashboard & user weather |
| **Profile Service** | 50053 | User profile management & preferences                        |
| **Weather Service** | 50052 | Real weather data via wttr.in API                            |
| **Hello Service**   | 50051 | Simple greeting service                                      |
| **Service A**       | N/A   | Pure gRPC client example                                     |

## Protocol Buffers

All services communicate using Protocol Buffers defined in:

- `proto/gateway.proto` - Gateway service definitions
- `proto/profile.proto` - User profile management
- `proto/weather.proto` - Weather data structures
- `proto/service.proto` - Hello service definitions

## Quick Start

### 1. Setup Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Generate gRPC Code

```powershell
.\generate_proto.ps1
```

### 3. Start Services

Open **4 separate terminals** and run:

```powershell
# Terminal 1 - Hello Service
python .\service_b\server.py

# Terminal 2 - Weather Service
python .\service_weather\server.py

# Terminal 3 - Profile Service
python .\service_profile\server.py

# Terminal 4 - Gateway Service
python .\service_gateway\server.py
```

### 4. Test gRPC Services

```powershell
# Run comprehensive gRPC tests
python test_grpc_client.py

# Or test Service A client
python .\service_a\app.py
```

## gRPC Service APIs

### Gateway Service (Port 50054)

```protobuf
service GatewayService {
  rpc GetDashboard (DashboardRequest) returns (DashboardReply) {}
  rpc GetUserWeather (UserWeatherRequest) returns (UserWeatherReply) {}
}
```

### Profile Service (Port 50053)

```protobuf
service ProfileService {
  rpc GetProfile (ProfileRequest) returns (ProfileReply) {}
  rpc UpdateCity (UpdateCityRequest) returns (UpdateCityReply) {}
}
```

### Weather Service (Port 50052)

```protobuf
service WeatherService {
  rpc GetWeather (WeatherRequest) returns (WeatherReply) {}
}
```

### Hello Service (Port 50051)

```protobuf
service HelloService {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}
```

## Testing Examples

### Manual gRPC Testing with Python

```python
import grpc
import gateway_pb2_grpc, gateway_pb2

# Test complete dashboard
with grpc.insecure_channel('localhost:50054') as channel:
    stub = gateway_pb2_grpc.GatewayServiceStub(channel)
    request = gateway_pb2.DashboardRequest(user_id="puneeth")
    response = stub.GetDashboard(request)
    print(f"Dashboard: {response}")

# Test user weather
with grpc.insecure_channel('localhost:50054') as channel:
    stub = gateway_pb2_grpc.GatewayServiceStub(channel)
    request = gateway_pb2.UserWeatherRequest(user_id="mohan")
    response = stub.GetUserWeather(request)
    print(f"User Weather: {response}")
```

### Using grpcurl (if installed)

```bash
# List services
grpcurl -plaintext localhost:50054 list

# Call dashboard
grpcurl -plaintext -d '{"user_id":"puneeth"}' localhost:50054 gateway.GatewayService/GetDashboard

# Call user weather
grpcurl -plaintext -d '{"user_id":"mohan"}' localhost:50054 gateway.GatewayService/GetUserWeather
```

## Sample Users

Pre-configured users for testing:

- `puneeth` - Bengaluru, IN
- `mohan` - Chennai, IN
- `ravi` - Bengaluru, IN
- `summit` - New York, US
- `john` - London, GB

## Performance Benefits

**Pure gRPC advantages:**

- ⚡ **Binary Protocol** - Faster than JSON/HTTP
- 🔄 **HTTP/2 Multiplexing** - Multiple requests per connection
- 📦 **Compact Payloads** - Protocol Buffer efficiency
- 🛡️ **Type Safety** - Compile-time schema validation
- 🌍 **Language Agnostic** - Works with any gRPC-supported language
- 🔗 **Streaming Support** - Bi-directional streaming capabilities

## Development

### Add New Service

1. Define service in `.proto` file
2. Regenerate code: `.\generate_proto.ps1`
3. Implement service class
4. Add server startup code
5. Update client tests

### Monitoring & Debugging

- Check server logs for request/response details
- Use gRPC reflection for service discovery
- Monitor connection health and latency
- Implement proper error handling and timeouts

## Production Considerations

- **Load Balancing**: Use gRPC load balancers
- **Security**: Enable TLS and authentication
- **Service Discovery**: Implement service registry
- **Monitoring**: Add metrics and distributed tracing
- **Resilience**: Circuit breakers and retries

---

**🎯 Pure gRPC = High Performance + Type Safety + Cross-Language Compatibility**
