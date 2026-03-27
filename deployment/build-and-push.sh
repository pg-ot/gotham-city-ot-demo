#!/bin/bash
# Build and Push All Docker Images to Docker Hub
# Usage: ./build-and-push.sh <dockerhub-username>

set -e

if [ -z "$1" ]; then
    echo "Usage: ./build-and-push.sh <dockerhub-username>"
    echo "Example: ./build-and-push.sh myusername"
    exit 1
fi

DOCKERHUB_USER=$1
VERSION="latest"

echo "=========================================="
echo "Building and Pushing Gotham City OT Demo"
echo "Docker Hub User: $DOCKERHUB_USER"
echo "=========================================="

# Login to Docker Hub
echo ""
echo "Please login to Docker Hub:"
docker login

# Build and push Breaker IED v1
echo ""
echo "Building Breaker IED v1..."
cd ../
docker build -f docker/Dockerfile.breaker-v1 -t ${DOCKERHUB_USER}/gotham-breaker-v1:${VERSION} .
docker push ${DOCKERHUB_USER}/gotham-breaker-v1:${VERSION}
echo "✓ Breaker IED v1 pushed"

# Build and push Breaker IED v2
echo ""
echo "Building Breaker IED v2..."
docker build -f docker/Dockerfile.breaker-v2 -t ${DOCKERHUB_USER}/gotham-breaker-v2:${VERSION} .
docker push ${DOCKERHUB_USER}/gotham-breaker-v2:${VERSION}
echo "✓ Breaker IED v2 pushed"

# Build and push Control IED
echo ""
echo "Building Control IED..."
docker build -f docker/Dockerfile.ied-simulator -t ${DOCKERHUB_USER}/gotham-control-ied:${VERSION} .
docker push ${DOCKERHUB_USER}/gotham-control-ied:${VERSION}
echo "✓ Control IED pushed"

# Build and push Central Monitoring
echo ""
echo "Building Central Monitoring Station..."
docker build -f central-monitoring/Dockerfile -t ${DOCKERHUB_USER}/gotham-central-monitoring:${VERSION} central-monitoring/
docker push ${DOCKERHUB_USER}/gotham-central-monitoring:${VERSION}
echo "✓ Central Monitoring pushed"

echo ""
echo "=========================================="
echo "All images built and pushed successfully!"
echo "=========================================="
echo ""
echo "Images available:"
echo "  - ${DOCKERHUB_USER}/gotham-breaker-v1:${VERSION}"
echo "  - ${DOCKERHUB_USER}/gotham-breaker-v2:${VERSION}"
echo "  - ${DOCKERHUB_USER}/gotham-control-ied:${VERSION}"
echo "  - ${DOCKERHUB_USER}/gotham-central-monitoring:${VERSION}"
echo ""
echo "External dependencies (already on Docker Hub):"
echo "  - pavi0204/openplc-with-message:latest"
echo "  - pavi0204/scadabr-with-message:golden"
echo "  - kalilinux/kali-last-release:latest"
echo ""
echo "Next steps:"
echo "1. Update docker-compose-ctf-final.yml with your Docker Hub username"
echo "2. Commit and push to GitHub"
echo "3. Users can pull and run: docker-compose up -d"
