# Git Commands for GitHub Deployment

## Step 1: Initialize Git Repository
```bash
cd "c:\Users\z003y2hc\Desktop\dt210324\Projects\2026\Null\Virtual Substation\ftc-master"
git init
git add .
git commit -m "Initial commit: Gotham City Industrial Grid - AI-Powered OT Attack Demo"
```

## Step 2: Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `gotham-city-ot-demo`
3. Description: "AI-powered OT attack demonstration - IEC 61850 GOOSE & Modbus TCP"
4. **Public** repository
5. **DO NOT** check "Add a README file"
6. Click "Create repository"

## Step 3: Link and Push to GitHub
```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git
git branch -M main
git push -u origin main
```

## Step 4: Verify Deployment (Test on Fresh Clone)
```bash
# Clone to a test directory
cd c:\temp
git clone https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git
cd gotham-city-ot-demo\deployment

# Start the demo
docker-compose up -d

# Check status
docker-compose ps

# Access Central Monitoring
# Open browser: http://localhost:5000
```

## Quick Commands Reference

### Check Git Status
```bash
git status
```

### View Commit History
```bash
git log --oneline
```

### Update Repository (After Changes)
```bash
git add .
git commit -m "Update: description of changes"
git push
```

### Stop Demo
```bash
cd deployment
docker-compose down
```

### Restart Demo
```bash
cd deployment
docker-compose restart
```

### View Logs
```bash
docker-compose logs -f central-monitoring
```

## Repository URL Format
After creation, your repository will be available at:
- **HTTPS**: `https://github.com/YOUR_USERNAME/gotham-city-ot-demo`
- **Clone URL**: `https://github.com/YOUR_USERNAME/gotham-city-ot-demo.git`
- **Web Interface**: `https://github.com/YOUR_USERNAME/gotham-city-ot-demo`

## Docker Hub Images
All images are already pushed to Docker Hub:
- `pavi0204/gotham-breaker-v1:latest`
- `pavi0204/gotham-breaker-v2:latest`
- `pavi0204/gotham-control-ied:latest`
- `pavi0204/gotham-central-monitoring:latest`
- `pavi0204/openplc-with-message:latest`
- `pavi0204/scadabr-with-message:golden`
- `kalilinux/kali-last-release:latest`

Users will automatically pull these images when running `docker-compose up -d`.
