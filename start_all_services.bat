@echo off
REM Multi-Microservice Commands for Windows
echo 🚀 Starting ALL gRPC Microservices...
echo.

REM Start all services in background
echo Starting Hello Service (Port 50051)...
start /B python service_b\server.py

echo Starting Weather Service (Port 50052)...
start /B python service_weather\server.py

echo Starting Profile Service (Port 50053)...
start /B python service_profile\server.py

echo Starting Gateway Service (Port 50054)...
start /B python service_gateway\server.py

echo.
echo ⏳ Waiting 3 seconds for services to start...
timeout /t 3 /nobreak >nul

echo.
echo ✅ All microservices started!
echo.
echo 🎯 Available Commands:
echo.
echo 1. Complete Dashboard (ALL services):
echo    python -c "import orchestrate_microservices as om; print(om.MicroserviceOrchestrator().get_complete_user_dashboard('puneeth'))"
echo.
echo 2. Multi-User Comparison:
echo    python orchestrate_microservices.py
echo.
echo 3. Individual Service Test:
echo    python test_grpc_client.py
echo.
echo Press any key to continue...
pause >nul