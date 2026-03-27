# Network Topology - Virtual Substation Demo

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Central Management Network: 10.10.10.0/24                  │
│  (Internet Access - For Kali & AI-Powered Attacks)          │
│                                                              │
│  ┌────────────────────────────────────────┐                 │
│  │  Kali Workstation: 10.10.10.5          │                 │
│  │  - SSH: localhost:2222                 │                 │
│  │  - Tools: nmap, scapy, tcpdump, etc.   │                 │
│  │  - Amazon Q / VS Code for AI attacks   │                 │
│  └────────┬──────────────────┬────────────┘                 │
└───────────┼──────────────────┼──────────────────────────────┘
            │                  │
            │ (Pivot)          │ (Pivot)
            │                  │
    ┌───────▼──────────┐   ┌───▼────────────────┐
    │  Substation      │   │  Industrial        │
    │  Segment         │   │  Process Segment   │
    │  192.168.100/24  │   │  192.168.200/24    │
    │  (ISOLATED)      │   │  (ISOLATED)        │
    │                  │   │                    │
    │  Kali IF:        │   │  Kali IF:          │
    │  192.168.100.6   │   │  192.168.200.6     │
    │                  │   │                    │
    │  ┌─────────────┐ │   │  ┌──────────────┐ │
    │  │ Breaker v1  │ │   │  │ OpenPLC      │ │
    │  │ .2:9001     │ │   │  │ .3:8080      │ │
    │  │ (Vulnerable)│ │   │  │ Modbus: 502  │ │
    │  └─────────────┘ │   │  └──────────────┘ │
    │                  │   │                    │
    │  ┌─────────────┐ │   │  ┌──────────────┐ │
    │  │ Breaker v2  │ │   │  │ ScadaBR      │ │
    │  │ .4:9002     │ │   │  │ .4:8080      │ │
    │  │ (Secure)    │ │   │  │ (SCADA HMI)  │ │
    │  └─────────────┘ │   │  └──────────────┘ │
    │                  │   │                    │
    │  ┌─────────────┐ │   │                    │
    │  │ Control IED │ │   │                    │
    │  │ (GOOSE Pub) │ │   │                    │
    │  └─────────────┘ │   │                    │
    └──────────────────┘   └────────────────────┘
         IEC 61850              Modbus TCP
         DNP3/GOOSE             EtherNet/IP
```

## Network Segments

### 1. Central Management Network (10.10.10.0/24)
- **Purpose**: Attacker/Demo workstation with internet access
- **Isolation**: NOT isolated - has internet for tool downloads
- **Key Asset**: Kali Linux (10.10.10.5)
- **Access**: SSH port 2222, Docker exec

### 2. Substation Segment (192.168.100.0/24)
- **Purpose**: Power substation IEDs and protection relays
- **Isolation**: ISOLATED from internet (internal: true)
- **Protocols**: IEC 61850, GOOSE, MMS
- **Assets**:
  - Breaker IED v1: 192.168.100.2 (Vulnerable)
  - Breaker IED v2: 192.168.100.4 (Secure)
  - Control IED: GOOSE publisher
  - Kali Interface: 192.168.100.6

### 3. Industrial Process Segment (192.168.200.0/24)
- **Purpose**: PLC and SCADA systems
- **Isolation**: ISOLATED from internet (internal: true)
- **Protocols**: Modbus TCP, EtherNet/IP
- **Assets**:
  - OpenPLC: 192.168.200.3 (Modbus port 502)
  - ScadaBR: 192.168.200.4 (SCADA HMI)
  - Kali Interface: 192.168.200.6

## Isolation Rules

```yaml
# Substation ↔ Industrial Process: NO DIRECT ROUTE
# Both segments are isolated from each other
# Only Kali can pivot between them (multi-homed)

attacker_network:  internal: false  # Internet access
ot_network:        internal: true   # Isolated
scada_network:     internal: true   # Isolated
```

## Attack Demo Flow (AI-Powered with Amazon Q)

### Phase 1: Reconnaissance
```bash
# From Kali (10.10.10.5)
nmap -sV 192.168.100.0/24  # Discover IEDs
nmap -sV 192.168.200.0/24  # Discover PLC/SCADA
```

### Phase 2: Substation Attack (IEC 61850)
```bash
# Target: Breaker v1 (192.168.100.2)
# Use Amazon Q to generate GOOSE injection attack
# Exploit: No sequence number validation
```

### Phase 3: Industrial Process Attack (Modbus)
```bash
# Target: OpenPLC (192.168.200.3:502)
# Use Amazon Q to generate Modbus manipulation
# Exploit: Unauthorized coil/register writes
```

### Phase 4: Lateral Movement
```bash
# Demonstrate pivot from Substation → Industrial
# Show how compromised IED can reach SCADA
```

## Access Points

### From Host Machine
- **Breaker v1 Web**: http://localhost:9001
- **Breaker v2 Web**: http://localhost:9002
- **OpenPLC**: http://localhost:8081 (openplc/openplc)
- **ScadaBR**: http://localhost:8080/ScadaBR (admin/admin)
- **Kali SSH**: ssh ctfuser@localhost -p 2222 (IEC61850_CTF_2024)

### From Kali Container
```bash
docker exec -it kali-workstation bash

# Substation targets
curl http://192.168.100.2:9000  # Breaker v1
curl http://192.168.100.4:9000  # Breaker v2

# Industrial targets
curl http://192.168.200.3:8080  # OpenPLC
curl http://192.168.200.4:8080  # ScadaBR
```

## Deployment Commands

```powershell
# Redeploy Kali with tools
.\redeploy-kali.ps1

# Check status
docker-compose -f docker-compose-ctf-final.yml ps

# View logs
docker-compose -f docker-compose-ctf-final.yml logs -f kali-workstation

# Access Kali
docker exec -it kali-workstation bash
```

## Demo Narrative

**Scenario**: Show how AI-powered tools (Amazon Q in VS Code) accelerate OT attacks, making them accessible even to less-skilled attackers.

**Key Points**:
1. Kali has multi-network access (simulating compromised jump host)
2. Substation and Industrial segments are isolated from each other
3. Use Amazon Q to generate attack code on-the-fly
4. Demonstrate speed: reconnaissance → exploit → impact in minutes
5. Show both IEC 61850 (substation) and Modbus (industrial) attacks

**Target Audience**: Security teams, OT engineers, management
**Message**: Traditional IT security skills + AI = Dangerous OT attacks
