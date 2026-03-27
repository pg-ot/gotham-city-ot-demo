# Virtual Substation - Current Deployment Status

## ✅ Successfully Deployed Components

### Network Segments (Isolated)

| Network | Subnet | Status | Purpose |
|---------|--------|--------|---------|
| `deployment_attacker_network` | 10.10.10.0/24 | ✅ Active | Central management (Kali - pending) |
| `deployment_ot_network` | 192.168.100.0/24 | ✅ Active | Substation IEDs (IEC 61850/GOOSE) |
| `deployment_scada_network` | 192.168.200.0/24 | ✅ Active | Industrial Process (PLC/SCADA) |

### Running Containers

#### Substation Segment (192.168.100.0/24)
1. **substation-breaker-v1** ✅
   - Port: 9001 → 9000
   - IP: 192.168.100.2
   - Type: Vulnerable IED (no sequence validation)
   - Protocol: IEC 61850 GOOSE
   - Access: http://localhost:9001

2. **substation-breaker-v2** ✅
   - Port: 9002 → 9000
   - IP: 192.168.100.4
   - Type: Secure IED (with stNum/sqNum validation)
   - Protocol: IEC 61850 GOOSE
   - Access: http://localhost:9002

3. **substation-control-ied** ✅
   - IP: 192.168.100.x
   - Type: Legitimate GOOSE publisher
   - Protocol: IEC 61850 GOOSE

#### Industrial Process Segment (192.168.200.0/24)
1. **openplc** ✅
   - Port: 8081 → 8080 (Web UI)
   - Port: 502 (Modbus TCP)
   - IP: 192.168.200.3
   - Credentials: openplc/openplc
   - Access: http://localhost:8081

2. **scadabr** ✅
   - Port: 8080 → 8080
   - IP: 192.168.200.4
   - Credentials: admin/admin
   - Access: http://localhost:8080/ScadaBR

#### Central Management (10.10.10.0/24)
1. **kali-workstation** ⏸️ PARKED
   - Status: Pending - proxy/SSL issues
   - Planned IP: 10.10.10.5
   - Multi-homed: Will connect to all 3 networks
   - Purpose: AI-powered attack demo platform

## Network Isolation Status

```
✅ Substation (192.168.100.0/24) ←→ Industrial (192.168.200.0/24): ISOLATED
✅ Both segments isolated from internet (internal: true in docker-compose)
⏸️ Kali pivot access: Pending deployment
```

## Demo Architecture

```
┌─────────────────────────────────────────┐
│  Central: 10.10.10.0/24                 │
│  [Kali - Parked]                        │
└────────┬──────────────┬─────────────────┘
         │              │
    ┌────▼─────┐   ┌────▼──────┐
    │ OT Net   │   │ SCADA Net │
    │ .100/24  │   │ .200/24   │
    │          │   │           │
    │ IEDs ✅  │   │ PLC ✅    │
    │ GOOSE    │   │ Modbus    │
    └──────────┘   └───────────┘
```

## Access Points (From Host)

### Substation Targets
- Breaker v1 (Vulnerable): http://localhost:9001
- Breaker v2 (Secure): http://localhost:9002

### Industrial Process Targets
- OpenPLC Web: http://localhost:8081 (openplc/openplc)
- OpenPLC Modbus: localhost:502
- ScadaBR: http://localhost:8080/ScadaBR (admin/admin)

## Next Steps for Kali

### Option 1: Use Pre-built Image with Tools
```bash
# Find a Kali image with tools pre-installed
docker pull offensive-security/kali-linux-docker
```

### Option 2: Manual Tool Installation (Post-deployment)
```bash
docker exec -it kali-workstation bash
# Install tools manually inside container
```

### Option 3: Use Ubuntu/Debian Base
```bash
# Use lighter base image and install specific OT tools
docker run -d --name kali-workstation ubuntu:latest
# Install: python3, scapy, nmap, etc.
```

### Option 4: Host-based Attack Demo
```bash
# Run attack scripts directly from Windows host
# Connect to containers via exposed ports
python attack_script.py --target localhost:9001
```

## Demo Flow (Without Kali for Now)

### Phase 1: Show Running Systems
1. Open http://localhost:8081 - Show OpenPLC running
2. Open http://localhost:8080/ScadaBR - Show SCADA HMI
3. Open http://localhost:9001 - Show IED status

### Phase 2: Network Isolation Demo
```powershell
# Show containers can't reach each other directly
docker exec openplc ping -c 2 192.168.100.2  # Should fail
docker exec substation-breaker-v1 ping -c 2 192.168.200.3  # Should fail
```

### Phase 3: AI-Powered Attack (From Host)
```powershell
# Use Amazon Q in VS Code to generate attack scripts
# Target exposed ports from Windows host
# Example: Modbus manipulation, GOOSE injection
```

## Management Commands

```powershell
# View all containers
docker-compose -f docker-compose-ctf-final.yml ps

# View logs
docker-compose -f docker-compose-ctf-final.yml logs -f

# Restart specific service
docker-compose -f docker-compose-ctf-final.yml restart openplc

# Stop all
docker-compose -f docker-compose-ctf-final.yml down

# Start all
docker-compose -f docker-compose-ctf-final.yml up -d
```

## Files Created

1. `docker-compose-ctf-final.yml` - Updated with network isolation
2. `NETWORK-TOPOLOGY.md` - Detailed architecture documentation
3. `DEPLOYMENT-STATUS.md` - This file
4. `deploy-kali-simple.ps1` - Kali deployment script (parked)
5. `redeploy-kali.ps1` - Alternative deployment script (parked)

## Summary

✅ **Working**: Substation and Industrial Process segments fully deployed and isolated
⏸️ **Parked**: Kali workstation (proxy/SSL certificate issues)
🎯 **Ready**: Can demo OT attacks from Windows host using exposed ports
🤖 **AI Demo**: Use Amazon Q to generate attack code targeting localhost ports
