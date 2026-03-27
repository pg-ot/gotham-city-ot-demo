# Gotham City Industrial Grid - AI-Powered OT Attack Demonstration

Demonstration environment showcasing how AI/GenAI shifts the barrier to entry for OT (Operational Technology) attacks across Skills, Means, Resources, and Motivation dimensions.

## Overview

This project demonstrates how AI tools like Amazon Q dramatically lower the skill barrier for attacking industrial control systems. It features Gotham City's critical infrastructure with two isolated OT networks:
- **Power Substation** (IEC 61850 GOOSE protocol)
- **Industrial Process Plant** (Modbus TCP protocol)

Both segments demonstrate how attackers with minimal domain knowledge can generate sophisticated exploits using AI assistance.

**Key Claim**: AI shifts Skills (STRONG), Means (HIGH), Resources (MODERATE), but Motivation (MINIMAL).

## Demo Purpose

Show that AI enables attackers to:
- Generate IEC 61850 GOOSE injection attacks against power substations without knowing the protocol
- Create Modbus TCP exploitation scripts against industrial plants without understanding control systems
- Compress attack timelines from weeks to minutes (480x faster)
- Lower skill requirements from expert to novice level

**Scenario**: Gotham City's power grid and industrial facilities under AI-assisted cyber attack
**Target Audience**: Security teams, OT engineers, management, policymakers

## Quick Start

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose
- 8GB RAM minimum
- Ports available: 5000, 8080, 8081, 9001, 9002, 502

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git
cd gotham-city-ot-demo/deployment

# Start all services
docker-compose up -d

# Wait 30 seconds for containers to start

# Verify deployment
docker-compose ps
```

### Verify Setup

```powershell
# Test Substation segment (IEC 61850)
curl http://localhost:9001/status

# Test Industrial segment (Modbus TCP)
python -c "from pymodbus.client import ModbusTcpClient; c=ModbusTcpClient('localhost',502); print('Modbus OK' if c.connect() else 'FAIL'); c.close()"

# Test OpenPLC web interface
curl http://localhost:8081
```

## Demo Access Points

### Visual Dashboard
- **Network Topology**: Open `network-topology.html` in browser
  - Shows all three network segments
  - Visual representation of isolation
  - Clickable links to live systems

### Live Systems
- **Breaker IED v1 (Vulnerable)**: http://localhost:9001
- **Breaker IED v2 (Secure)**: http://localhost:9002
- **OpenPLC Runtime**: http://localhost:8081 (openplc/openplc)
- **ScadaBR SCADA**: http://localhost:8080/ScadaBR (admin/admin)
- **Modbus TCP**: localhost:502

### Attack Scripts
- **Modbus Attack Demo**: `python modbus_attack_demo.py`
- **AI Prompt Templates**: See `MODBUS-ATTACK-PROMPTS.md`
- **GOOSE Attack**: Generate with Amazon Q (see demo script)

## Running the Demo

### Full Demo (18-22 minutes)

1. **Open Demo Materials**
   ```powershell
   # Open network topology visualization
   start network-topology.html
   
   # Open demo script
   code DEMO-SCRIPT.md
   
   # Open quick reference
   code DEMO-QUICK-REFERENCE.md
   ```

2. **Phase 1: Setup (3-4 min)**
   - Show network-topology.html
   - Explain three isolated segments
   - Click through to show live systems

3. **Phase 2: GOOSE Attack - Skills Shift (5-6 min)**
   - Use Amazon Q to generate IEC 61850 GOOSE injection attack
   - Execute against Breaker IED v1
   - Show breaker tripping
   - **Message**: Zero protocol knowledge → Working exploit in 30 seconds

4. **Phase 3: Modbus Attack - Means Shift (6-8 min)**
   - Use Amazon Q to generate Modbus TCP attack (see MODBUS-ATTACK-PROMPTS.md)
   - Execute: `python modbus_attack.py`
   - Show OpenPLC registers modified
   - **Message**: AI generates custom tooling on-demand

5. **Phase 4: Discuss Shifts (3 min)**
   - Skills: Expert → Novice (STRONG)
   - Means: Manual → AI-generated (HIGH)
   - Resources: 480x faster, but still need access (MODERATE)
   - Motivation: Unchanged (MINIMAL)

### Quick Demo (12 minutes)
Skip detailed explanations, focus on live attacks and key metrics.

### Demo Files
- `DEMO-SCRIPT.md` - Complete walkthrough with timing
- `DEMO-QUICK-REFERENCE.md` - One-page cheat sheet
- `MODBUS-ATTACK-PROMPTS.md` - AI prompts for Modbus attacks
- `modbus_attack_demo.py` - Pre-built Modbus attack script
- `network-topology.html` - Visual network diagram

## Network Architecture

### Three Isolated Segments

```
┌─────────────────────────────────────────┐
│  Central Management: 10.10.10.0/24      │
│  (Kali workstation - parked)            │
└────────┬──────────────┬─────────────────┘
         │              │
    ┌────▼─────┐   ┌────▼──────┐
    │ OT Net   │   │ SCADA Net │
    │ .100/24  │   │ .200/24   │
    │ ISOLATED │   │ ISOLATED  │
    └──────────┘   └───────────┘
```

### 1. Central Management Network (10.10.10.0/24)
- **Purpose**: Attack/demo workstation with internet access
- **Status**: Kali container parked (proxy issues)
- **Note**: Attacks can be run from Windows host via exposed ports

### 2. Power Substation Segment (192.168.100.0/24)
**Protocol**: IEC 61850 GOOSE (Layer 2 multicast)
**Isolation**: No internet, no access to Industrial segment
**Location**: Gotham City East End Substation

| Device | IP | Port | Description |
|--------|-----|------|-------------|
| Breaker IED v1 | 192.168.100.2 | 9001 | Vulnerable (no sequence validation) |
| Breaker IED v2 | 192.168.100.4 | 9002 | Secure (stNum/sqNum validated) |
| Control IED | 192.168.100.x | - | GOOSE publisher (1s heartbeat) |

**Attack Surface**: GOOSE replay attacks, packet injection
**Impact**: Power outage affecting East End district (42,000 residents)

### 3. Industrial Process Plant Segment (192.168.200.0/24)
**Protocol**: Modbus TCP (Port 502)
**Isolation**: No internet, no access to Substation segment
**Location**: Gotham City Industrial District (Wayne Enterprises Manufacturing)

| Device | IP | Port | Description |
|--------|-----|------|-------------|
| OpenPLC | 192.168.200.3 | 8081, 502 | PLC runtime, Modbus server |
| ScadaBR | 192.168.200.4 | 8080 | SCADA HMI interface |

**Attack Surface**: Modbus coil/register manipulation, unauthorized writes
**Impact**: Production line disruption, equipment damage, safety hazards

## AI-Powered Attack Demonstrations

### Attack 1: IEC 61850 GOOSE Injection (Skills Shift)
**Target**: Gotham City East End Substation

**Traditional Approach:****
- Study IEC 61850 standard (1000+ pages)
- Learn GOOSE protocol structure
- Understand stNum/sqNum sequencing
- Craft packets with scapy
- **Time**: 2-4 weeks

**AI-Assisted Approach:**
```
Amazon Q Prompt: "Generate Python script to inject IEC 61850 GOOSE 
trip command to breaker at 192.168.100.2:9001"
```
- AI generates complete exploit in 30 seconds
- Execute immediately
- **Time**: 2 minutes

**Skills Shift**: Expert (IEC 61850) → Novice (basic Python) = **STRONG**

### Attack 2: Modbus TCP Manipulation (Means Shift)
**Target**: Gotham City Industrial District (Wayne Enterprises)

**Traditional Approach:****
- Study Modbus specification
- Learn function codes (0x01, 0x03, 0x05, 0x06, etc.)
- Find or write Modbus library
- Craft read/write operations
- **Time**: Days to weeks

**AI-Assisted Approach:**
```
Amazon Q Prompt: "Create Modbus attack script: read registers 0-10, 
write 9999 to register 0, force coil 0 ON. Target: localhost:502"
```
- AI generates complete attack workflow
- Includes reconnaissance, exploitation, verification
- **Time**: 60 seconds

**Means Shift**: Manual tool hunting → AI-generated custom exploits = **HIGH**

### Key Metrics

| Metric | Traditional | AI-Assisted | Shift |
|--------|-------------|-------------|-------|
| Time to exploit | 4-8 weeks | 10 minutes | **480x faster** |
| Skill required | Expert (protocols) | Basic (Python) | **Strong** |
| Tool development | Days (manual) | Minutes (AI) | **High** |
| Cost | High (expertise) | Low (AI sub) | **Moderate** |
| Motivation | Unchanged | Unchanged | **Minimal** |

## Project Structure

```
Gotham City Industrial Grid/
├── deployment/
│   ├── docker-compose-ctf-final.yml  # Main deployment config
│   ├── DEPLOYMENT-STATUS.md          # Current setup status
│   ├── NETWORK-TOPOLOGY.md           # Technical architecture
│   └── trip.sh / close.sh            # Breaker control scripts
├── DEMO-SCRIPT.md                    # Complete demo walkthrough (18-22 min)
├── DEMO-QUICK-REFERENCE.md           # One-page cheat sheet
├── MODBUS-ATTACK-PROMPTS.md          # AI prompts for Modbus attacks
├── modbus_attack_demo.py             # Pre-built Modbus attack script
├── network-topology.html             # Visual network diagram
├── dashboard.html                    # Original Purdue model dashboard
├── src/
│   ├── libiec61850/                  # IEC 61850 library (submodule)
│   ├── breaker_ied_v1.c              # Vulnerable breaker
│   ├── breaker_ied_v2.c              # Secure breaker
│   ├── control_ied.c                 # GOOSE publisher
│   └── flag_server_v*.py             # Web interfaces
└── docker/
    ├── Dockerfile.breaker-v1
    ├── Dockerfile.breaker-v2
    ├── Dockerfile.ied-simulator
    └── Dockerfile.kali
```

## Container Management

### Start/Stop
```powershell
cd deployment

# Start all containers
docker-compose -f docker-compose-ctf-final.yml up -d

# Stop all containers
docker-compose -f docker-compose-ctf-final.yml down

# Restart specific container
docker restart openplc
docker restart substation-breaker-v1

# View logs
docker-compose -f docker-compose-ctf-final.yml logs -f
```

### Status Check
```powershell
# List running containers
docker-compose -f docker-compose-ctf-final.yml ps

# Check networks
docker network ls --filter name=deployment

# Verify isolation
docker exec openplc ping -c 2 192.168.100.2  # Should fail (isolated)
```

## Learning Objectives

### Technical Skills
- Understand IEC 61850 GOOSE protocol vulnerabilities
- Learn Modbus TCP attack techniques
- Practice network segmentation concepts
- Analyze OT protocol security weaknesses

### Strategic Understanding
- Recognize how AI lowers barrier to entry for OT attacks
- Understand the shift in Skills, Means, Resources, Motivation
- Appreciate the compression of attack timelines (weeks → minutes)
- Identify defense strategies in an AI-enabled threat landscape

### Key Takeaways
1. **AI doesn't create attackers** - it amplifies existing ones
2. **Skill barrier collapsed** - novices can execute expert-level attacks
3. **Time compression** - 480x faster attack development
4. **Motivation unchanged** - intent remains the same, capability increases
5. **Defense imperative** - assume breach, detect anomalies, use AI for defense

## Troubleshooting

### Containers Not Starting
```powershell
# Check logs
docker logs substation-breaker-v1
docker logs openplc

# Rebuild if needed
cd deployment
docker-compose -f docker-compose-ctf-final.yml build --no-cache
docker-compose -f docker-compose-ctf-final.yml up -d
```

### Port Conflicts
```powershell
# Check if ports are in use
netstat -an | findstr ":9001 :9002 :8080 :8081 :502"

# Change ports in docker-compose-ctf-final.yml if needed
```

### Modbus Connection Issues
```powershell
# Test Modbus connectivity
python -c "from pymodbus.client import ModbusTcpClient; c=ModbusTcpClient('localhost',502); print('OK' if c.connect() else 'FAIL')"

# Install pymodbus if missing
pip install pymodbus

# Restart OpenPLC
docker restart openplc
```

### Network Isolation Not Working
```powershell
# Recreate networks
cd deployment
docker-compose -f docker-compose-ctf-final.yml down
docker network prune
docker-compose -f docker-compose-ctf-final.yml up -d
```

### Kali Workstation Issues
**Status**: Parked due to corporate proxy/SSL issues
**Workaround**: Run attacks from Windows host using exposed ports
**Note**: Attacks work identically from host - demonstrates that specialized infrastructure isn't needed

## Documentation

- **DEMO-SCRIPT.md** - Complete demo walkthrough with timing (18-22 min)
- **DEMO-QUICK-REFERENCE.md** - One-page cheat sheet for live demo
- **MODBUS-ATTACK-PROMPTS.md** - AI prompts for generating Modbus attacks
- **DEPLOYMENT-STATUS.md** - Current deployment status and access points
- **NETWORK-TOPOLOGY.md** - Detailed technical architecture
- **network-topology.html** - Visual network diagram (open in browser)
- **dashboard.html** - Original Purdue model dashboard

## Demo Preparation Checklist

- [ ] All containers running (5/5)
- [ ] pymodbus installed: `pip install pymodbus`
- [ ] VS Code with Amazon Q enabled
- [ ] network-topology.html open in browser
- [ ] DEMO-QUICK-REFERENCE.md open for reference
- [ ] Test connectivity to all systems
- [ ] Practice AI prompts once before live demo

## Expected Demo Flow

1. **Setup** (3 min) → Show topology, explain isolation
2. **GOOSE Attack** (5 min) → AI generates IEC 61850 exploit
3. **Modbus Attack** (6 min) → AI generates Modbus exploit
4. **Discussion** (3 min) → Explain shifts in Skills/Means/Resources
5. **Q&A** (5 min) → Address questions

**Total**: 20-25 minutes

## Security & Ethics

- **Educational Purpose Only** - Never attack real OT/ICS systems
- **Responsible Disclosure** - Report real vulnerabilities through proper channels
- **Intentional Vulnerabilities** - All weaknesses are designed for learning
- **Defense Awareness** - Use knowledge to improve security, not cause harm
- **AI Ethics** - Demonstrate risks to drive better defenses, not enable attacks

## Credits

Repurposed from IEC 61850 CTF challenge for AI-powered OT attack demonstration.

**Original Purpose**: CTF competition  
**Current Purpose**: AI capability shift demonstration  
**Scenario**: Gotham City critical infrastructure  
**Target Audience**: Security professionals, OT engineers, policymakers

## License

Educational and demonstration use only.
