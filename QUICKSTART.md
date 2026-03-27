# Quick Start Guide

Get the Gotham City Industrial Grid demo running in 5 minutes.

## Prerequisites

- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- Docker Compose installed
- 8GB RAM minimum
- 20GB free disk space

## Option 1: Use Pre-built Images (Recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git
cd gotham-city-ot-demo/deployment
```

### Step 2: Update Docker Compose File

Edit `docker-compose.yml` and replace `YOUR_DOCKERHUB_USERNAME` with the actual Docker Hub username where images are hosted.

**Example:**
```yaml
# Before
image: YOUR_DOCKERHUB_USERNAME/gotham-breaker-v1:latest

# After (if images are at dockerhub.com/u/johndoe)
image: johndoe/gotham-breaker-v1:latest
```

### Step 3: Start All Services

```bash
docker-compose up -d
```

Wait 30 seconds for all containers to start.

### Step 4: Verify Deployment

```bash
docker-compose ps
```

You should see 7 containers running:
- substation-breaker-v1
- substation-breaker-v2
- substation-control-ied
- openplc
- scadabr
- central-monitoring
- kali-workstation

### Step 5: Access Systems

Open in your browser:
- **Central Monitoring**: http://localhost:5000
- **Breaker IED v1**: http://localhost:9001
- **Breaker IED v2**: http://localhost:9002
- **OpenPLC**: http://localhost:8081 (openplc/openplc)
- **ScadaBR**: http://localhost:8080/ScadaBR (admin/admin)

## Option 2: Build Images Locally

### Step 1: Clone Repository with Submodules

```bash
git clone --recurse-submodules https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git
cd gotham-city-ot-demo/deployment
```

### Step 2: Use Local Build Compose File

```bash
docker-compose -f docker-compose-ctf-final.yml up -d --build
```

This will build all images locally (takes 5-10 minutes).

## Troubleshooting

### Containers Not Starting

```bash
# Check logs
docker-compose logs

# Restart specific container
docker-compose restart central-monitoring
```

### Port Conflicts

If ports 5000, 8080, 8081, 9001, 9002, or 502 are already in use:

Edit `docker-compose.yml` and change the host port (left side):
```yaml
ports:
  - "5001:5000"  # Changed from 5000:5000
```

### Images Not Found

Make sure you've replaced `YOUR_DOCKERHUB_USERNAME` in `docker-compose.yml` with the correct username.

Or build locally using `docker-compose-ctf-final.yml`.

## Next Steps

1. **View Network Topology**: Open `network-topology.html` in browser
2. **Read Demo Script**: See `DEMO-SCRIPT.md` for full walkthrough
3. **Try Attacks**: Follow `LATERAL-MOVEMENT-DEMO.md`
4. **Install Python Tools**: `pip install pymodbus` for Modbus attacks

## Stopping the Demo

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8GB | 16GB |
| CPU | 4 cores | 8 cores |
| Disk | 20GB | 50GB |
| OS | Windows 10, macOS 10.15, Ubuntu 20.04 | Latest versions |

## Support

- **Issues**: Open an issue on GitHub
- **Documentation**: See README.md for full details
- **Demo Guide**: DEMO-SCRIPT.md for presentation walkthrough

## Quick Commands Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart service
docker-compose restart central-monitoring

# Check status
docker-compose ps

# Access Kali
docker exec -it kali-workstation bash

# View Central Monitoring API
curl http://localhost:5000/api/status
```
