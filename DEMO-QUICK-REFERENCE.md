# Demo Quick Reference Card
## AI-Powered OT Attacks: Skills, Means, Resources Shift

---

## ⏱️ TIMING: 18-22 Minutes

| Phase | Topic | Time | Key Message |
|-------|-------|------|-------------|
| 1 | Setup | 3-4 min | Show isolated networks, live systems |
| 2 | GOOSE Attack | 5-6 min | **Skills Shift: STRONG** - Zero IEC 61850 knowledge → Working exploit |
| 3 | Modbus Attack | 6-8 min | **Means Shift: HIGH** - AI generates custom tooling on-demand |
| 4 | Resources | 2-3 min | **Resources Shift: MODERATE** - Faster, but still need access |
| 5 | Motivation | 1-2 min | **Motivation Shift: MINIMAL** - AI amplifies, doesn't create attackers |

---

## 🎯 TWO ATTACK DEMONSTRATIONS

### Attack 1: IEC 61850 GOOSE Injection (Skills Shift)
- **Target**: Breaker IED v1 at localhost:9001
- **Protocol**: IEC 61850 GOOSE (Layer 2 multicast)
- **Vulnerability**: No sequence number validation
- **AI Prompt**: "Generate Python script to inject GOOSE trip command to breaker at 192.168.100.2:9001"
- **Impact**: Breaker trips, 42,000 customers lose power
- **Skill Barrier**: Expert (IEC 61850 spec) → Novice (basic Python)

### Attack 2: Modbus TCP Manipulation (Means Shift)
- **Target**: OpenPLC at localhost:502
- **Protocol**: Modbus TCP (industrial control)
- **Vulnerability**: No authentication, plaintext
- **AI Prompt**: "Create Modbus attack script: read registers 0-10, write 9999 to register 0, force coil 0 ON"
- **Impact**: Emergency stop triggered, setpoints manipulated
- **Tool Barrier**: Manual tool hunting → AI generates custom exploit

---

## 📋 PRE-DEMO CHECKLIST

### Containers Running (5/5)
```powershell
docker ps --format "{{.Names}}\t{{.Status}}"
```
- [ ] substation-breaker-v1 (Port 9001)
- [ ] substation-breaker-v2 (Port 9002)
- [ ] substation-control-ied
- [ ] openplc (Ports 8081, 502)
- [ ] scadabr (Port 8080)

### Browser Tabs Open
- [ ] network-topology.html (visual demo)
- [ ] http://localhost:9001 (Breaker v1 status)
- [ ] http://localhost:8081 (OpenPLC interface)

### Tools Ready
- [ ] VS Code with Amazon Q enabled
- [ ] Python with pymodbus installed: `pip install pymodbus`
- [ ] PowerShell terminal ready
- [ ] MODBUS-ATTACK-PROMPTS.md open for reference

### Test Connectivity
```powershell
# Test Breaker
curl http://localhost:9001/status

# Test Modbus
python -c "from pymodbus.client import ModbusTcpClient; c=ModbusTcpClient('localhost',502); print('OK' if c.connect() else 'FAIL')"
```

---

## 🎤 KEY TALKING POINTS

### Opening Hook
> "Traditionally, attacking OT systems requires rare expertise: IEC 61850, Modbus, DNP3.
> Today, I'll show you how AI collapses that barrier in minutes."

### After GOOSE Attack
> "I just went from zero IEC 61850 knowledge to a working exploit in 30 seconds.
> **Skills Shift: STRONG** - The barrier to OT-relevant knowledge just collapsed."

### After Modbus Attack
> "AI didn't just give me code - it gave me custom attack tooling, generated on-demand.
> **Means Shift: HIGH** - Attack automation is now conversational."

### Resources Discussion
> "Execution is 480x faster, but I still need network access, persistence, infrastructure.
> **Resources Shift: MODERATE** - Efficiency improves, constraints remain."

### Closing Statement
> "AI doesn't change WHO attacks or WHY they attack.
> It changes HOW EASILY they can attack and HOW FAST they adapt.
> When the barrier to entry drops this low, we don't need more motivated attackers.
> We just need more attackers. And that's the real threat."

---

## 🔥 LIVE DEMO FLOW

### 1. Show Network Topology (2 min)
- Open network-topology.html
- Point out: "3 isolated segments, Kali can pivot (parked for now)"
- Click through to show live systems

### 2. GOOSE Attack with AI (5 min)
**Amazon Q Prompt:**
```
Generate a Python script to inject an IEC 61850 GOOSE trip command 
to a breaker IED at 192.168.100.2 port 9001. The breaker should 
trip (open) when it receives the malicious GOOSE frame.
```
- Show AI generating code (30 sec)
- Execute: `python goose_attack.py`
- Show breaker tripped on dashboard
- **Message**: "Zero knowledge → Working exploit in 30 seconds"

### 3. Modbus Attack with AI (6 min)
**Amazon Q Prompt:**
```
Create a complete Modbus TCP attack script for OpenPLC at localhost:502 that:

Phase 1 - Reconnaissance:
- Read and display current state of registers 0-10
- Read and display current state of coils 0-10

Phase 2 - Exploitation:
- Force coil 0 to ON (emergency stop)
- Write 9999 to register 0 (setpoint override)
- Write malicious values to registers 0-4

Phase 3 - Verification:
- Read back modified values to confirm attack success

Use pymodbus library and include clear status messages for each phase.
```
- Show AI generating complete attack workflow
- Execute: `python modbus_attack.py`
- Show output with phases
- Open OpenPLC web interface to verify
- **Message**: "Custom tooling, generated in 60 seconds"

### 4. Discuss Shifts (3 min)
- **Skills**: Expert → Novice (STRONG)
- **Means**: Manual → AI-generated (HIGH)
- **Resources**: Faster execution, same constraints (MODERATE)
- **Motivation**: Unchanged (MINIMAL)

### 5. Close with Impact (1 min)
- Show metrics: 480x faster, skill barrier collapsed
- "The gap between novice and expert just closed"

---

## 📊 KEY METRICS

| Metric | Traditional | AI-Assisted | Multiplier |
|--------|-------------|-------------|------------|
| Time to exploit | 4-8 weeks | 10 minutes | **480x faster** |
| Skill required | Expert (IEC 61850, Modbus) | Basic (Python, prompting) | **Strong shift** |
| Tool development | Days (manual coding) | Minutes (AI generation) | **High shift** |
| Adaptation speed | Days (debugging) | Minutes (AI fixes) | **High shift** |
| Cost | High (rare expertise) | Low (AI subscription) | **Moderate shift** |

---

## 🚨 TROUBLESHOOTING

### If Breaker Doesn't Trip
```powershell
docker restart substation-breaker-v1
docker logs substation-breaker-v1 --tail 20
```

### If Modbus Connection Fails
```powershell
# Check port
netstat -an | findstr ":502"

# Restart OpenPLC
docker restart openplc

# Test connection
python -c "from pymodbus.client import ModbusTcpClient; c=ModbusTcpClient('localhost',502); print(c.connect())"
```

### If pymodbus Not Installed
```powershell
pip install pymodbus
# or
python -m pip install pymodbus
```

### If Demo Completely Fails
**Fallback**: Show pre-written scripts and explain:
> "Even if execution fails, the point stands: AI generated this exploit code in seconds.
> That's the capability shift we're demonstrating - not the technical execution."

---

## 🎯 BACKUP CONTENT (If Extra Time)

### Show AI Adaptation
- Introduce an error (wrong port)
- Prompt: "The script failed with [error], fix it"
- Show AI debugging in real-time

### Show AI Explanation
- Prompt: "Explain how this GOOSE attack works in simple terms"
- Show AI lowering knowledge barrier further

### Show Multiple Protocols
- "AI can generate attacks for DNP3, BACnet, EtherNet/IP..."
- "It's not protocol-specific - it's capability-general"

---

## 📝 Q&A PREP

**Q: "Can't we just block AI tools?"**
A: "AI is a capability, not a product. Open-source models, offline tools - genie is out."

**Q: "What's the defense?"**
A: "Assume breach. Network segmentation, anomaly detection, zero-trust. Defenders need AI too."

**Q: "Is this realistic?"**
A: "Yes. Real protocols, real vulnerabilities, real attack patterns. Only difference: 10 minutes vs 10 weeks."

**Q: "What about Kali being parked?"**
A: "Attacks work from any machine with network access. That's the point - no specialized infrastructure needed."

---

## ✅ SUCCESS CRITERIA

- [ ] Demonstrated AI generating IEC 61850 exploit
- [ ] Demonstrated AI generating Modbus exploit
- [ ] Showed both attacks executing successfully
- [ ] Explained all four shifts (Skills, Means, Resources, Motivation)
- [ ] Delivered key message: "Barrier to entry collapsed"
- [ ] Stayed within 20-minute timeframe

---

## 🎬 FINAL CHECKLIST

Before starting:
- [ ] All containers running
- [ ] All browser tabs open
- [ ] VS Code ready with Amazon Q
- [ ] pymodbus installed
- [ ] network-topology.html loaded
- [ ] MODBUS-ATTACK-PROMPTS.md open
- [ ] Confident with timing and flow

**You're ready! Good luck with the demo! 🚀**
