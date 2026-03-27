# Deployment Directory

This directory contains everything needed to deploy the Gotham City Industrial Grid demo.

## Quick Start

### For Users (Deploy Pre-Built Images)
```bash
docker-compose up -d
```

That's it! All images will be pulled from Docker Hub automatically.

### For Developers (Build and Push Images)

**Windows:**
```powershell
.\build-and-push.ps1 -DockerHubUser YOUR_DOCKERHUB_USERNAME
```

**Linux/Mac:**
```bash
chmod +x build-and-push.sh
./build-and-push.sh YOUR_DOCKERHUB_USERNAME
```

## Files in This Directory

### Docker Compose Files
- **`docker-compose.yml`** - Production deployment file (uses pavi0204 images)
- **`docker-compose-ctf-final.yml`** - Original CTF version with all configurations

### Build Scripts
- **`build-and-push.ps1`** - Windows PowerShell script to build and push images
- **`build-and-push.sh`** - Linux/Mac bash script to build and push images

### Legacy Scripts (From CTF Version)
- `deploy.sh` - Original deployment script
- `close.sh` / `close.ps1` - Stop all containers
- `status.sh` - Check container status
- `trip.sh` / `trip.ps1` - Trigger breaker trip

## Network Architecture

The demo creates three isolated networks:

1. **Central Management** (10.10.10.0/24)
   - Central Monitoring Station
   - Kali Workstation

2. **Substation/OT** (192.168.100.0/24)
   - Breaker IED v1 (Vulnerable)
   - Breaker IED v2 (Secured)
   - Control IED
   - Central Monitoring Station (multi-homed)
   - Kali Workstation (multi-homed)

3. **Industrial/SCADA** (192.168.200.0/24)
   - OpenPLC (Modbus TCP)
   - ScadaBR (SCADA HMI)
   - Central Monitoring Station (multi-homed)
   - Kali Workstation (multi-homed)

## Services and Ports

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Central Monitoring | 5000 | http://localhost:5000 | Main dashboard & attack entry |
| Breaker v1 | 9001 | http://localhost:9001 | Vulnerable GOOSE breaker |
| Breaker v2 | 9002 | http://localhost:9002 | Secured GOOSE breaker |
| OpenPLC | 8081 | http://localhost:8081 | Modbus TCP PLC |
| ScadaBR | 8080 | http://localhost:8080/ScadaBR | SCADA HMI |
| Kali | - | docker exec | Attacker workstation |
| Control IED | - | Internal only | GOOSE publisher |

## Common Commands

### Start Demo
```bash
docker-compose up -d
```

### Stop Demo
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
docker-compose logs -f central-monitoring
```

### Check Status
```bash
docker-compose ps
```

### Restart Service
```bash
docker-compose restart central-monitoring
```

### Access Kali Container
```bash
docker exec -it kali-workstation bash
```

## Troubleshooting

### Ports Already in Use
If you see "port already allocated" errors:
```bash
# Stop conflicting services
docker-compose down

# Or change ports in docker-compose.yml
```

### Images Not Found
If images fail to pull:
```bash
# Verify Docker Hub connectivity
docker pull pavi0204/gotham-breaker-v1:latest

# Or build locally
cd ..
docker build -f docker/Dockerfile.breaker-v1 -t pavi0204/gotham-breaker-v1:latest .
```

### Containers Not Starting
```bash
# Check logs
docker-compose logs

# Restart specific service
docker-compose restart SERVICE_NAME
```

### Network Issues
```bash
# Recreate networks
docker-compose down
docker network prune
docker-compose up -d
```

## Docker Hub Images

All images are hosted on Docker Hub under `pavi0204`:

- `pavi0204/gotham-breaker-v1:latest`
- `pavi0204/gotham-breaker-v2:latest`
- `pavi0204/gotham-control-ied:latest`
- `pavi0204/gotham-central-monitoring:latest`
- `pavi0204/openplc-with-message:latest`
- `pavi0204/scadabr-with-message:golden`
- `kalilinux/kali-last-release:latest`

## Documentation

For complete documentation, see:
- `../QUICKSTART.md` - 5-minute setup guide
- `../DEMO-SCRIPT.md` - Full demo walkthrough
- `../README.md` - Complete project documentation

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs: `docker-compose logs`
3. Verify all containers are running: `docker-compose ps`
4. See main README.md for detailed documentation

## License

MIT License - See `../LICENSE` for details

**⚠️ EDUCATIONAL USE ONLY** - Never attack real ICS systems
