# Central Monitoring Station

## Overview

The Central Monitoring Station is a Flask-based web application that bridges all three network segments in the Gotham City Industrial Grid. It aggregates real-time data from:
- **East End Substation** (192.168.100.0/24) - IEC 61850 GOOSE devices
- **Industrial District** (192.168.200.0/24) - Modbus TCP PLC/SCADA

## Purpose in Demo

This container serves as the **ATTACK ENTRY POINT** for the Kali workstation, demonstrating:
1. **Multi-network access** - Bridges isolated OT segments
2. **Internet exposure** - Accessible from outside (port 5000)
3. **Data aggregation** - Collects information from all segments
4. **Realistic attack vector** - Mimics real-world DMZ/monitoring systems

## Network Configuration

The Central Monitoring Station has interfaces on all three networks:

| Network | IP Address | Purpose |
|---------|------------|---------|
| Attacker Network | 10.10.10.10 | Internet-facing, Kali access point |
| OT Network | 192.168.100.10 | Access to Substation IEDs |
| SCADA Network | 192.168.200.10 | Access to PLC/SCADA systems |

## Access

- **Dashboard**: http://localhost:5000
- **API**: http://localhost:5000/api/status
- **Health Check**: http://localhost:5000/health

## Features

### Real-time Monitoring
- Polls all devices every 3 seconds
- Displays online/offline status
- Shows device-specific data (breaker position, PLC status, etc.)

### API Endpoints

#### GET /
Returns HTML dashboard with live updates

#### GET /api/status
Returns JSON with aggregated status:
```json
{
  "timestamp": "2026-03-28T01:30:00",
  "summary": {
    "total_devices": 6,
    "online_devices": 6
  },
  "substation": {
    "breaker_v1": {
      "online": true,
      "data": "Position: CLOSED | stNum: 6"
    },
    "breaker_v2": {
      "online": true,
      "data": "Position: CLOSED | stNum: 8"
    }
  },
  "industrial": {
    "openplc": {
      "online": true,
      "data": "PLC Active | Modbus: 192.168.200.3:502"
    },
    "scadabr": {
      "online": true,
      "data": "SCADA HMI Active"
    }
  }
}
```

## Attack Scenario

### Step 1: Compromise Central Monitoring
Attacker gains access to the monitoring station (simulated by Kali having network access)

### Step 2: Pivot to OT Networks
From Central Monitoring (10.10.10.10), attacker can reach:
- Substation devices at 192.168.100.x
- Industrial devices at 192.168.200.x

### Step 3: Lateral Movement
Use Central Monitoring as a jump host to attack isolated OT segments

## Demo Narrative

> "This Central Monitoring Station is exposed to the internet for remote access.
> It bridges all three network segments to aggregate data.
> While convenient for operations, it's a perfect entry point for attackers.
> Once compromised, it provides access to both isolated OT networks.
> This is exactly how real-world OT breaches happen - through poorly secured DMZ systems."

## Technical Details

### Built With
- Python 3.11
- Flask 3.0.0
- Requests library for HTTP polling

### Container Specs
- **Image**: Custom Python Flask app
- **Ports**: 5000 (HTTP)
- **Networks**: All three (attacker, ot, scada)
- **Resources**: 512MB RAM, 0.5 CPU

### Data Collection
The monitoring station actively polls:
- `http://192.168.100.2:9000/status` (Breaker v1)
- `http://192.168.100.4:9000/status` (Breaker v2)
- `http://192.168.200.3:8080/` (OpenPLC)
- `http://192.168.200.4:8080/ScadaBR/` (ScadaBR)

## Security Implications

### Vulnerabilities Demonstrated
1. **No Authentication** - Dashboard is publicly accessible
2. **Multi-network Bridge** - Breaks network isolation
3. **Information Disclosure** - Exposes network topology and device status
4. **Pivot Point** - Can be used to reach isolated networks

### Real-World Parallels
- Industrial DMZ systems
- Remote monitoring platforms
- Vendor access portals
- Cloud-connected SCADA gateways

## Deployment

Already included in `docker-compose-ctf-final.yml`:

```yaml
central-monitoring:
  build:
    context: ../central-monitoring
  ports:
    - "5000:5000"
  networks:
    attacker_network:
      ipv4_address: 10.10.10.10
    ot_network:
      ipv4_address: 192.168.100.10
    scada_network:
      ipv4_address: 192.168.200.10
```

Start with:
```bash
docker-compose -f docker-compose-ctf-final.yml up -d central-monitoring
```

## Logs

View real-time logs:
```bash
docker logs -f central-monitoring
```

## Integration with Kali

Kali workstation (10.10.10.5) can:
1. Access Central Monitoring dashboard at http://10.10.10.10:5000
2. Use it as reconnaissance to discover OT devices
3. Pivot through it to reach isolated networks
4. Exploit the multi-network access for lateral movement

## Files

- `app.py` - Flask application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container build instructions
- `README.md` - This file
