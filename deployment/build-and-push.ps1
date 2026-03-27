# Build and Push All Docker Images to Docker Hub
# Usage: .\build-and-push.ps1 -DockerHubUser <username>

param(
    [Parameter(Mandatory=$true)]
    [string]$DockerHubUser
)

$VERSION = "latest"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Building and Pushing Gotham City OT Demo" -ForegroundColor Cyan
Write-Host "Docker Hub User: $DockerHubUser" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Login to Docker Hub
Write-Host "`nPlease login to Docker Hub:" -ForegroundColor Yellow
docker login

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker login failed!" -ForegroundColor Red
    exit 1
}

# Build and push Breaker IED v1
Write-Host "`nBuilding Breaker IED v1..." -ForegroundColor Yellow
Set-Location ..
docker build -f docker/Dockerfile.breaker-v1 -t ${DockerHubUser}/gotham-breaker-v1:${VERSION} .
docker push ${DockerHubUser}/gotham-breaker-v1:${VERSION}
Write-Host "✓ Breaker IED v1 pushed" -ForegroundColor Green

# Build and push Breaker IED v2
Write-Host "`nBuilding Breaker IED v2..." -ForegroundColor Yellow
docker build -f docker/Dockerfile.breaker-v2 -t ${DockerHubUser}/gotham-breaker-v2:${VERSION} .
docker push ${DockerHubUser}/gotham-breaker-v2:${VERSION}
Write-Host "✓ Breaker IED v2 pushed" -ForegroundColor Green

# Build and push Control IED
Write-Host "`nBuilding Control IED..." -ForegroundColor Yellow
docker build -f docker/Dockerfile.ied-simulator -t ${DockerHubUser}/gotham-control-ied:${VERSION} .
docker push ${DockerHubUser}/gotham-control-ied:${VERSION}
Write-Host "✓ Control IED pushed" -ForegroundColor Green

# Build and push Central Monitoring
Write-Host "`nBuilding Central Monitoring Station..." -ForegroundColor Yellow
docker build -f central-monitoring/Dockerfile -t ${DockerHubUser}/gotham-central-monitoring:${VERSION} central-monitoring/
docker push ${DockerHubUser}/gotham-central-monitoring:${VERSION}
Write-Host "✓ Central Monitoring pushed" -ForegroundColor Green

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "All images built and pushed successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

Write-Host "`nImages available:" -ForegroundColor White
Write-Host "  - ${DockerHubUser}/gotham-breaker-v1:${VERSION}"
Write-Host "  - ${DockerHubUser}/gotham-breaker-v2:${VERSION}"
Write-Host "  - ${DockerHubUser}/gotham-control-ied:${VERSION}"
Write-Host "  - ${DockerHubUser}/gotham-central-monitoring:${VERSION}"

Write-Host "`nExternal dependencies (already on Docker Hub):" -ForegroundColor White
Write-Host "  - pavi0204/openplc-with-message:latest"
Write-Host "  - pavi0204/scadabr-with-message:golden"
Write-Host "  - kalilinux/kali-last-release:latest"

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Update docker-compose-ctf-final.yml with your Docker Hub username"
Write-Host "2. Commit and push to GitHub"
Write-Host "3. Users can pull and run: docker-compose up -d"
