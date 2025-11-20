@echo off
echo =====================================
echo Multi-Microservice Commands (FIXED)
echo =====================================
echo.

echo 1. Complete User Dashboard (ALL 4 services):
echo    python simple_orchestrator.py dashboard puneeth
echo.

echo 2. Multi-User Comparison:
echo    python simple_orchestrator.py compare puneeth mohan john
echo.

echo 3. Weather Aggregation:
echo    python simple_orchestrator.py weather Mumbai Delhi London "New York"
echo.

echo 4. Full Test Suite:
echo    python orchestrate_microservices.py
echo.

echo 5. Individual Service Test:
echo    python test_grpc_client.py
echo.

echo =====================================
echo Choose a command to run:
echo =====================================
echo.
set /p choice="Enter 1, 2, 3, 4, or 5: "

if "%choice%"=="1" (
    echo Running: Complete User Dashboard...
    python simple_orchestrator.py dashboard puneeth
) else if "%choice%"=="2" (
    echo Running: Multi-User Comparison...
    python simple_orchestrator.py compare puneeth mohan john
) else if "%choice%"=="3" (
    echo Running: Weather Aggregation...
    python simple_orchestrator.py weather Mumbai Delhi London "New York"
) else if "%choice%"=="4" (
    echo Running: Full Test Suite...
    python orchestrate_microservices.py
) else if "%choice%"=="5" (
    echo Running: Individual Service Test...
    python test_grpc_client.py
) else (
    echo Invalid choice!
)

echo.
pause