# PowerShell script to start all microservices and run orchestration commands
Write-Host "🚀 Multi-Microservice Orchestration Commands" -ForegroundColor Green
Write-Host "=" * 50

# Function to start services
function Start-AllServices {
    Write-Host "`n📡 Starting ALL gRPC Microservices..." -ForegroundColor Yellow
    
    $jobs = @()
    
    $jobs += Start-Job -ScriptBlock { 
        Set-Location "E:\allthing\New folder\grpc"
        & "E:\allthing\New folder\grpc\.venv\Scripts\Activate.ps1"
        python service_b\server.py 
    } -Name "HelloService"
    
    $jobs += Start-Job -ScriptBlock { 
        Set-Location "E:\allthing\New folder\grpc"
        & "E:\allthing\New folder\grpc\.venv\Scripts\Activate.ps1"
        python service_weather\server.py 
    } -Name "WeatherService"
    
    $jobs += Start-Job -ScriptBlock { 
        Set-Location "E:\allthing\New folder\grpc"
        & "E:\allthing\New folder\grpc\.venv\Scripts\Activate.ps1"
        python service_profile\server.py 
    } -Name "ProfileService"
    
    $jobs += Start-Job -ScriptBlock { 
        Set-Location "E:\allthing\New folder\grpc"
        & "E:\allthing\New folder\grpc\.venv\Scripts\Activate.ps1"
        python service_gateway\server.py 
    } -Name "GatewayService"
    
    Write-Host "⏳ Waiting 5 seconds for services to initialize..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    Write-Host "✅ All microservices started as background jobs!" -ForegroundColor Green
    return $jobs
}

# Function to show orchestration commands
function Show-OrchestrationCommands {
    Write-Host "`n🎯 MULTI-MICROSERVICE COMMANDS:" -ForegroundColor Cyan
    Write-Host "-" * 40
    
    Write-Host "`n1️⃣  Complete User Dashboard (ALL 4 services):" -ForegroundColor White
    Write-Host "   python orchestrate_microservices.py" -ForegroundColor Yellow
    
    Write-Host "`n2️⃣  Single User Dashboard:" -ForegroundColor White  
    Write-Host "   python -c `"exec(open('orchestrate_microservices.py').read()); print(MicroserviceOrchestrator().get_complete_user_dashboard('puneeth'))`"" -ForegroundColor Yellow
    
    Write-Host "`n3️⃣  Multi-User Weather Comparison:" -ForegroundColor White
    Write-Host "   python -c `"exec(open('orchestrate_microservices.py').read()); print(MicroserviceOrchestrator().get_multi_user_comparison(['puneeth', 'mohan']))`"" -ForegroundColor Yellow
    
    Write-Host "`n4️⃣  Weather Aggregation (Multiple Cities):" -ForegroundColor White
    Write-Host "   python -c `"exec(open('orchestrate_microservices.py').read()); print(MicroserviceOrchestrator().get_weather_aggregation(['Mumbai', 'London', 'Delhi']))`"" -ForegroundColor Yellow
    
    Write-Host "`n5️⃣  Individual Service Tests:" -ForegroundColor White
    Write-Host "   python test_grpc_client.py" -ForegroundColor Yellow
}

# Main execution
try {
    $serviceJobs = Start-AllServices
    Show-OrchestrationCommands
    
    Write-Host "`n💡 TIP: Use these commands to connect multiple microservices!" -ForegroundColor Green
    Write-Host "📊 Each command orchestrates different service combinations for unified output." -ForegroundColor Green
    
    Write-Host "`nPress Enter to stop all services..." -ForegroundColor Red
    Read-Host
    
    # Cleanup
    Write-Host "🛑 Stopping all microservices..." -ForegroundColor Red
    $serviceJobs | Stop-Job
    $serviceJobs | Remove-Job
    Write-Host "✅ All services stopped." -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}