# Deploy Kali with pre-built image
Write-Host "=== Deploying Kali Workstation (Pre-built Image) ===" -ForegroundColor Cyan

# Stop and remove existing Kali container
Write-Host "Stopping existing kali-workstation..." -ForegroundColor Yellow
docker stop kali-workstation 2>$null
docker rm kali-workstation 2>$null

# Pull and start Kali container
Write-Host "Starting kali-workstation with tools..." -ForegroundColor Yellow
docker-compose -f docker-compose-ctf-final.yml up -d kali-workstation

# Wait for container to be ready and tools to install
Write-Host "Waiting for tools installation (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verify network interfaces
Write-Host "`n=== Network Configuration ===" -ForegroundColor Cyan
docker exec kali-workstation ip -br addr 2>$null

Write-Host "`n=== Installed Tools Check ===" -ForegroundColor Cyan
docker exec kali-workstation which nmap 2>$null
docker exec kali-workstation which curl 2>$null
docker exec kali-workstation which python3 2>$null

Write-Host "`n=== Testing Connectivity ===" -ForegroundColor Cyan
Write-Host "Substation Network (192.168.100.0/24):" -ForegroundColor Yellow
docker exec kali-workstation ping -c 2 192.168.100.2 2>$null
docker exec kali-workstation ping -c 2 192.168.100.4 2>$null

Write-Host "`nIndustrial Process Network (192.168.200.0/24):" -ForegroundColor Yellow
docker exec kali-workstation ping -c 2 192.168.200.3 2>$null
docker exec kali-workstation ping -c 2 192.168.200.4 2>$null

Write-Host "`n=== Kali Access ===" -ForegroundColor Cyan
Write-Host "Shell: docker exec -it kali-workstation bash" -ForegroundColor Green

Write-Host "`n=== Network Topology ===" -ForegroundColor Cyan
Write-Host "Central (Kali):     10.10.10.5" -ForegroundColor White
Write-Host "Substation:         192.168.100.6 (IEDs, GOOSE)" -ForegroundColor Green
Write-Host "Industrial Process: 192.168.200.6 (PLC, SCADA)" -ForegroundColor Magenta

Write-Host "`n=== Quick Test Commands ===" -ForegroundColor Cyan
Write-Host "docker exec kali-workstation nmap -sn 192.168.100.0/24" -ForegroundColor Gray
Write-Host "docker exec kali-workstation nmap -sn 192.168.200.0/24" -ForegroundColor Gray
Write-Host "docker exec kali-workstation curl http://192.168.100.2:9000" -ForegroundColor Gray
