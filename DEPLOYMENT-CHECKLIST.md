# Deployment Checklist for GitHub and Docker Hub

## Pre-Deployment Steps

### 1. Build and Test Locally

```bash
cd deployment
docker-compose -f docker-compose-ctf-final.yml up -d --build
```

Verify all 7 containers are running:
- [ ] substation-breaker-v1
- [ ] substation-breaker-v2
- [ ] substation-control-ied
- [ ] openplc
- [ ] scadabr
- [ ] central-monitoring
- [ ] kali-workstation

Test all access points:
- [ ] http://localhost:5000 (Central Monitoring)
- [ ] http://localhost:9001 (Breaker v1)
- [ ] http://localhost:9002 (Breaker v2)
- [ ] http://localhost:8081 (OpenPLC)
- [ ] http://localhost:8080/ScadaBR (ScadaBR)

### 2. Build and Push Docker Images

**Option A: Manual Push**

```bash
cd deployment

# Windows
.\build-and-push.ps1 -DockerHubUser YOUR_USERNAME

# Linux/Mac
chmod +x build-and-push.sh
./build-and-push.sh YOUR_USERNAME
```

**Option B: GitHub Actions (Automated)**

1. Add secrets to GitHub repository:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Docker Hub access token

2. Push to GitHub - images will build automatically

### 3. Update docker-compose.yml

Replace `YOUR_DOCKERHUB_USERNAME` with your actual username:

```bash
# Linux/Mac
sed -i 's/YOUR_DOCKERHUB_USERNAME/yourusername/g' deployment/docker-compose.yml

# Windows PowerShell
(Get-Content deployment/docker-compose.yml) -replace 'YOUR_DOCKERHUB_USERNAME', 'yourusername' | Set-Content deployment/docker-compose.yml
```

### 4. Verify Images on Docker Hub

Check that all images are available:
- [ ] https://hub.docker.com/r/YOUR_USERNAME/gotham-breaker-v1
- [ ] https://hub.docker.com/r/YOUR_USERNAME/gotham-breaker-v2
- [ ] https://hub.docker.com/r/YOUR_USERNAME/gotham-control-ied
- [ ] https://hub.docker.com/r/YOUR_USERNAME/gotham-central-monitoring

## GitHub Repository Setup

### 1. Initialize Git (if not already done)

```bash
cd "c:\Users\z003y2hc\Desktop\dt210324\Projects\2026\Null\Virtual Substation\ftc-master"
git init
git add .
git commit -m "Initial commit: Gotham City OT Demo"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `gotham-city-ot-demo`
3. Description: "AI-Powered OT Attack Demonstration - Gotham City Industrial Grid"
4. Public or Private (your choice)
5. Don't initialize with README (we have one)

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git
git branch -M main
git push -u origin main
```

### 4. Update README.md

Replace placeholders in README.md:
- [ ] Update clone URL with your GitHub username
- [ ] Update Docker Hub image references
- [ ] Add your contact information

## Post-Deployment Verification

### 1. Test Fresh Clone

On a different machine or clean directory:

```bash
git clone https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git
cd gotham-city-ot-demo/deployment
docker-compose up -d
```

Wait 30 seconds, then verify:

```bash
docker-compose ps
curl http://localhost:5000/api/status
```

### 2. Test All Access Points

- [ ] Central Monitoring: http://localhost:5000
- [ ] All 6 devices showing online
- [ ] Breaker status accessible
- [ ] OpenPLC accessible
- [ ] ScadaBR accessible

### 3. Test Demo Flow

Follow `DEMO-SCRIPT.md`:
- [ ] Network topology visible
- [ ] Can access Kali container
- [ ] Can reach OT devices from Kali
- [ ] Modbus attack works
- [ ] GOOSE attack works (if applicable)

## Documentation Checklist

Ensure all files are present and updated:

- [ ] README.md - Main documentation
- [ ] QUICKSTART.md - Quick start guide
- [ ] DEMO-SCRIPT.md - Full demo walkthrough
- [ ] DEMO-QUICK-REFERENCE.md - One-page cheat sheet
- [ ] MODBUS-ATTACK-PROMPTS.md - AI prompts for Modbus
- [ ] LATERAL-MOVEMENT-DEMO.md - Attack flow documentation
- [ ] DEPLOYMENT-STATUS.md - Current deployment info
- [ ] NETWORK-TOPOLOGY.md - Technical architecture
- [ ] network-topology.html - Visual diagram
- [ ] dashboard.html - Purdue model dashboard
- [ ] .gitignore - Git ignore file
- [ ] LICENSE - License file (if applicable)

## Docker Hub Image Checklist

All images should be public and have:

- [ ] Clear description
- [ ] Tags: `latest`
- [ ] README with usage instructions
- [ ] Links to GitHub repository

## GitHub Repository Checklist

- [ ] README.md is clear and comprehensive
- [ ] All documentation files committed
- [ ] .gitignore properly configured
- [ ] GitHub Actions workflow configured (optional)
- [ ] Repository topics added: `ot-security`, `ics`, `scada`, `docker`, `cybersecurity`
- [ ] License file added (if applicable)

## Final Verification Commands

```bash
# Pull and run on fresh system
git clone https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git
cd gotham-city-ot-demo/deployment
docker-compose up -d

# Wait 30 seconds
sleep 30

# Verify all containers
docker-compose ps

# Test Central Monitoring
curl http://localhost:5000/api/status | jq

# Test Breaker
curl http://localhost:9001/status

# Test OpenPLC
curl http://localhost:8081

# Clean up
docker-compose down
```

## Troubleshooting

### Images Not Found
- Verify Docker Hub username is correct in docker-compose.yml
- Check images are public on Docker Hub
- Try: `docker pull YOUR_USERNAME/gotham-breaker-v1:latest`

### Containers Not Starting
- Check logs: `docker-compose logs`
- Verify port availability: `netstat -an | findstr "5000 8080 8081 9001 9002 502"`
- Check system resources: Docker Desktop → Settings → Resources

### Submodules Missing
- Clone with: `git clone --recurse-submodules <repo-url>`
- Or after clone: `git submodule update --init --recursive`

## Success Criteria

✅ Repository cloned successfully
✅ All images pulled from Docker Hub
✅ All 7 containers running
✅ All web interfaces accessible
✅ Central Monitoring shows 6 devices online
✅ Demo script works end-to-end
✅ Documentation is clear and complete

## Support

If users encounter issues:
1. Check GitHub Issues
2. Review QUICKSTART.md
3. Verify system requirements
4. Check Docker logs
5. Open new issue with details
