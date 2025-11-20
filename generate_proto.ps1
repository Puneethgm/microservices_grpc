python -m grpc_tools.protoc --proto_path=proto --python_out=. --grpc_python_out=. proto/service.proto proto/weather.proto proto/profile.proto

if ($LASTEXITCODE -eq 0) {
    Write-Host "Generated Python gRPC files:"
    Write-Host "  - service_pb2.py and service_pb2_grpc.py"
    Write-Host "  - weather_pb2.py and weather_pb2_grpc.py"
    Write-Host "  - profile_pb2.py and profile_pb2_grpc.py"
} else {
    Write-Host "protoc failed with exit code $LASTEXITCODE"
}