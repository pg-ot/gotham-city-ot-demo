#!/bin/bash

# Multi-Team CTF Deployment Script
# Deploys isolated environments for multiple teams

set -e

NUM_TEAMS=${1:-1}

echo "=========================================="
echo "Multi-Team CTF Deployment"
echo "Deploying $NUM_TEAMS team(s)"
echo "=========================================="
echo ""
echo "Cleaning up existing containers..."

# Stop and remove conflicting containers
docker stop $(docker ps -a --filter "name=substation" -q) 2>/dev/null || true
docker rm $(docker ps -a --filter "name=substation" -q) 2>/dev/null || true
docker stop $(docker ps -a --filter "name=team" -q) 2>/dev/null || true
docker rm $(docker ps -a --filter "name=team" -q) 2>/dev/null || true
docker stop openplc scadabr kali-workstation 2>/dev/null || true
docker rm openplc scadabr kali-workstation 2>/dev/null || true

# Remove conflicting networks
docker network rm deployment_ot_network deployment_scada_network 2>/dev/null || true
docker network rm $(docker network ls --filter "name=team" -q) 2>/dev/null || true

echo "✓ Cleanup complete"
echo ""

# Base ports
BASE_BREAKER_V1_PORT=9001
BASE_BREAKER_V2_PORT=9002
BASE_OPENPLC_WEB_PORT=8081
BASE_SCADABR_PORT=8080
BASE_MODBUS_PORT=502
BASE_SSH_PORT=20000

# Base networks
BASE_OT_SUBNET=100
BASE_SCADA_SUBNET=200

for i in $(seq 1 $NUM_TEAMS); do
    echo ""
    echo "Deploying Team $i..."
    
    # Calculate ports
    BREAKER_V1_PORT=$((BASE_BREAKER_V1_PORT + (i - 1) * 10))
    BREAKER_V2_PORT=$((BASE_BREAKER_V2_PORT + (i - 1) * 10))
    OPENPLC_WEB_PORT=$((BASE_OPENPLC_WEB_PORT + (i - 1) * 10))
    SCADABR_PORT=$((BASE_SCADABR_PORT + (i - 1) * 10))
    MODBUS_PORT=$((BASE_MODBUS_PORT + (i - 1) * 10))
    SSH_PORT=$((BASE_SSH_PORT + i))
    
    # Calculate subnets
    OT_SUBNET=$((BASE_OT_SUBNET + i))
    SCADA_SUBNET=$((BASE_SCADA_SUBNET + i))
    
    # Create networks
    docker network create --subnet=192.168.${OT_SUBNET}.0/24 team${i}_ot_network 2>/dev/null || true
    docker network create --subnet=192.168.${SCADA_SUBNET}.0/24 team${i}_scada_network 2>/dev/null || true
    
    # Deploy breaker-ied-v1
    docker run -d \
        --name team${i}-breaker-v1 \
        --network team${i}_ot_network \
        --ip 192.168.${OT_SUBNET}.4 \
        -p ${BREAKER_V1_PORT}:9000 \
        --cap-add NET_RAW \
        --cap-add NET_ADMIN \
        --restart unless-stopped \
        pavi0204/breaker-ied-v1:golden \
        ./start.sh
    
    # Deploy breaker-ied-v2
    docker run -d \
        --name team${i}-breaker-v2 \
        --network team${i}_ot_network \
        --ip 192.168.${OT_SUBNET}.2 \
        -p ${BREAKER_V2_PORT}:9000 \
        --cap-add NET_RAW \
        --cap-add NET_ADMIN \
        --restart unless-stopped \
        pavi0204/breaker-ied-v2:golden \
        ./start.sh
    
    # Deploy control-ied
    docker run -d \
        --name team${i}-control-ied \
        --network team${i}_ot_network \
        --ip 192.168.${OT_SUBNET}.3 \
        --cap-add NET_RAW \
        --cap-add NET_ADMIN \
        --restart unless-stopped \
        pavi0204/control-ied:golden \
        ./control_ied
    
    # Deploy OpenPLC
    docker run -d \
        --name team${i}-openplc \
        --network team${i}_scada_network \
        --network-alias openplc \
        --ip 192.168.${SCADA_SUBNET}.3 \
        -p ${OPENPLC_WEB_PORT}:8080 \
        -p ${MODBUS_PORT}:502 \
        --restart unless-stopped \
        pavi0204/openplc-with-message:latest
    
    # Deploy ScadaBR
    docker run -d \
        --name team${i}-scadabr \
        --network team${i}_scada_network \
        --ip 192.168.${SCADA_SUBNET}.4 \
        -p ${SCADABR_PORT}:8080 \
        --restart unless-stopped \
        pavi0204/scadabr-with-message:latest
    
    # Deploy Kali workstation (dual-homed)
    docker run -d \
        --name team${i}-kali \
        --network team${i}_ot_network \
        --ip 192.168.${OT_SUBNET}.5 \
        -p ${SSH_PORT}:22 \
        --cap-add=NET_ADMIN \
        --cap-add=NET_RAW \
        --restart unless-stopped \
        pavi0204/kali-ctf:sshd
    
    # Ensure ctfuser exists with default password
    docker exec team${i}-kali bash -c "useradd -m -s /bin/bash ctfuser 2>/dev/null || true; echo 'ctfuser:IEC61850_CTF_2024' | chpasswd; usermod -aG sudo ctfuser; /usr/sbin/sshd 2>/dev/null || true" || true
    
    # Connect Kali to second network
    docker network connect --ip 192.168.${SCADA_SUBNET}.2 team${i}_scada_network team${i}-kali
    
    echo "✓ Team $i deployed"
    echo "  Breaker v1: http://localhost:${BREAKER_V1_PORT}"
    echo "  Breaker v2: http://localhost:${BREAKER_V2_PORT}"
    echo "  OpenPLC:    http://localhost:${OPENPLC_WEB_PORT}"
    echo "  ScadaBR:    http://localhost:${SCADABR_PORT}/ScadaBR"
    echo "  Kali SSH:   ssh root@localhost -p ${SSH_PORT}"
done

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "$NUM_TEAMS team(s) deployed successfully"
echo "=========================================="
