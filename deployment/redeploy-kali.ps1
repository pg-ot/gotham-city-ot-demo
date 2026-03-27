# Redeploy Kali with proper tools and network isolation
Write-Host "=== Redeploying Kali Workstation ===" -ForegroundColor Cyan

# Stop and remove existing Kali container
Write-Host "Stopping kali-workstation..." -ForegroundColor Yellow
docker stop kali-workstation
docker rm kali-workstation

# Rebuild Kali image with tools
Write-Host "Building Kali image with tools..." -ForegroundColor Yellow
docker-compose -f docker-compose-ctf-final.yml build kali-workstation

# Start Kali container
Write-Host "Starting kali-workstation..." -ForegroundColor Yellow
docker-compose -f docker-compose-ctf-final.yml up -d kali-workstation

# Wait for container to be ready
Start-Sleep -Seconds 5

# Verify network interfaces
Write-Host "`n=== Network Configuration ===" -ForegroundColor Cyan
docker exec kali-workstation ip -br addr

Write-Host "`n=== Testing Connectivity ===" -ForegroundColor Cyan
Write-Host "Substation Network (192.168.100.0/24):" -ForegroundColor Yellow
docker exec kali-workstation ping -c 2 192.168.100.2 2>$null
docker exec kali-workstation ping -c 2 192.168.100.4 2>$null

Write-Host "`nIndustrial Process Network (192.168.200.0/24):" -ForegroundColor Yellow
docker exec kali-workstation ping -c 2 192.168.200.3 2>$null
docker exec kali-workstation ping -c 2 192.168.200.4 2>$null

Write-Host "`n=== Kali Access ===" -ForegroundColor Cyan
Write-Host "SSH: ssh ctfuser@localhost -p 2222" -ForegroundColor Green
Write-Host "Password: IEC61850_CTF_2024" -ForegroundColor Green
Write-Host "Shell: docker exec -it kali-workstation bash" -ForegroundColor Green

Write-Host "`n=== Network Topology ===" -ForegroundColor Cyan
Write-Host "Central (Kali):     10.10.10.5" -ForegroundColor White
Write-Host "Substation:         192.168.100.6 (IEDs, GOOSE)" -ForegroundColor Green
Write-Host "Industrial Process: 192.168.200.6 (PLC, SCADA)" -ForegroundColor Magenta
