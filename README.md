# Flask + gRPC Microservices:

## 🏗️ Architecture

This project showcases 5 microservices communicating via gRPC:

- **`service_gateway`** (Port 5000) - API Gateway orchestrating all services
- **`service_a`** (Port 5002) - Simple greeting service (original example)
- **`service_b`** (Port 5001) - Hello service with gRPC server (Port 50051)
- **`service_weather`** (Port 5003) - Weather data via wttr.in API + gRPC (Port 50052)
- **`service_profile`** (Port 5004) - User profiles with gRPC (Port 50053)

## 📁 Project Structure

```
grpc/
├── proto/
│   ├── service.proto          # Hello service definition
│   ├── weather.proto          # Weather service definition
│   └── profile.proto          # Profile service definition
├── service_gateway/
│   └── app.py                 # API Gateway (orchestrates all services)
├── service_a/
│   └── app.py                 # Simple Flask client
├── service_b/
│   └── server.py              # Hello gRPC + HTTP server
├── service_weather/
│   └── server.py              # Weather gRPC + HTTP server
├── service_profile/
│   └── server.py              # Profile gRPC + HTTP server
├── generate_proto.ps1         # Generate gRPC Python code
├── requirements.txt           # Dependencies
└── README.md                  
```

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

### 3. Start All Services

Open 5 separate terminals and run:

```powershell
# Terminal 1 - Hello Service
python .\service_b\server.py

# Terminal 2 - Weather Service
python .\service_weather\server.py

# Terminal 3 - Profile Service
python .\service_profile\server.py

# Terminal 4 - Original Service A
python .\service_a\app.py

# Terminal 5 - API Gateway
python .\service_gateway\app.py
```

##  Testing Examples

```powershell
# Simple greeting (original example)
Invoke-RestMethod http://localhost:5002/hello/puneeth

# Weather for any city
Invoke-RestMethod http://localhost:5000/weather/London

# User profile
Invoke-RestMethod http://localhost:5000/user/puneeth
```
```powershell
# Weather for user's preferred city
Invoke-RestMethod http://localhost:5000/user/puneeth/weather

# Complete dashboard (calls 3 services)
Invoke-RestMethod http://localhost:5000/dashboard/puneeth
```

## 📊 API Endpoints

### API Gateway (localhost:5000)

- `GET /` - Service information
- `GET /hello/<name>` - Greeting via hello service
- `GET /weather/<city>` - Weather for any city
- `GET /user/<user_id>` - User profile
- `GET /user/<user_id>/weather` - Weather for user's city
- `GET /dashboard/<user_id>` - Complete dashboard

### Individual Services

- **Service A**: `localhost:5002/hello/<name>`
- **Service B**: `localhost:5001/`
- **Weather**: `localhost:5003/weather/<city>`
- **Profile**: `localhost:5004/profile/<user_id>`

## 👥 Sample Users

Pre-configured users for testing:

- `puneeth` - Bengaluru, IN

## 🔧 gRPC Service Details

- **Hello Service** (Port 50051): Simple greeting messages
- **Weather Service** (Port 50052): Real weather data from wttr.in API
- **Profile Service** (Port 50053): User preferences and data


## Test Commands

```powershell
# Test the complete flow - dashboard for puneeth
Invoke-RestMethod http://localhost:5000/dashboard/puneeth

# Test weather service
Invoke-RestMethod http://localhost:5000/weather/Mumbai

# Test user preferences
Invoke-RestMethod http://localhost:5000/user/alice/weather

# Original simple example
Invoke-RestMethod http://localhost:5002/hello/puneeth
```