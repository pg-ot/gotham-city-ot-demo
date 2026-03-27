from flask import Flask, jsonify, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Gotham City Central Monitoring Station</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #0a0e12 0%, #1a1e22 100%);
            color: #b8c4d0;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 30px;
            background: rgba(26, 30, 34, 0.8);
            border-radius: 12px;
            margin-bottom: 30px;
            border: 2px solid #3a4454;
        }
        .header h1 {
            font-size: 32px;
            color: #e6c25e;
            margin-bottom: 10px;
        }
        .status-bar {
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            gap: 20px;
        }
        .status-card {
            flex: 1;
            background: rgba(26, 30, 34, 0.8);
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #3a4454;
            text-align: center;
        }
        .status-card h3 {
            font-size: 14px;
            color: #7a8494;
            margin-bottom: 10px;
        }
        .status-card .value {
            font-size: 28px;
            font-weight: bold;
            color: #4a8a4a;
        }
        .segments {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        .segment {
            background: rgba(26, 30, 34, 0.8);
            border-radius: 12px;
            padding: 24px;
            border: 2px solid #3a4454;
        }
        .segment-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid #3a4454;
        }
        .segment-icon { font-size: 32px; }
        .segment-title h2 { font-size: 18px; color: #e6c25e; }
        .segment-title p { font-size: 12px; color: #7a8494; }
        .device {
            background: rgba(0, 0, 0, 0.3);
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            border-left: 3px solid #4a8a4a;
        }
        .device.offline {
            border-left-color: #8a4a4a;
            opacity: 0.6;
        }
        .device-name {
            font-size: 14px;
            font-weight: 600;
            color: #b8c4d0;
        }
        .device-status { font-size: 11px; color: #7a8494; }
        .device-data {
            font-size: 12px;
            color: #9aa4b2;
            margin-top: 8px;
            font-family: 'Courier New', monospace;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #5a6a7a;
            font-size: 12px;
        }
        .refresh-time {
            text-align: center;
            color: #5a6a7a;
            font-size: 11px;
            margin-bottom: 20px;
        }
        .vulnerability-badge {
            display: inline-block;
            background: #8a4a4a;
            color: #fff;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 10px;
            margin-left: 8px;
        }
    </style>
    <script>
        async function fetchData() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateDashboard(data);
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function updateDashboard(data) {
            document.getElementById('total-devices').textContent = data.summary.total_devices;
            document.getElementById('online-devices').textContent = data.summary.online_devices;
            updateDevice('breaker-v1', data.substation.breaker_v1);
            updateDevice('breaker-v2', data.substation.breaker_v2);
            updateDevice('openplc', data.industrial.openplc);
            updateDevice('scadabr', data.industrial.scadabr);
            document.getElementById('last-update').textContent = 'Last updated: ' + new Date().toLocaleTimeString();
        }

        function updateDevice(id, device) {
            const element = document.getElementById(id);
            if (!element) return;
            if (device.online) {
                element.classList.remove('offline');
                element.querySelector('.device-status').textContent = '● Online';
                element.querySelector('.device-data').textContent = device.data || 'No data';
            } else {
                element.classList.add('offline');
                element.querySelector('.device-status').textContent = '○ Offline';
                element.querySelector('.device-data').textContent = 'Connection failed';
            }
        }

        setInterval(fetchData, 3000);
        fetchData();
    </script>
</head>
<body>
    <div class="header">
        <h1>🏙️ Gotham City Central Monitoring Station</h1>
        <p>Real-time monitoring · East End Substation & Industrial District</p>
    </div>

    <div class="status-bar">
        <div class="status-card">
            <h3>Total Devices</h3>
            <div class="value" id="total-devices">6</div>
        </div>
        <div class="status-card">
            <h3>Online</h3>
            <div class="value" id="online-devices">-</div>
        </div>
    </div>

    <div class="refresh-time" id="last-update">Connecting...</div>

    <div class="segments">
        <div class="segment">
            <div class="segment-header">
                <div class="segment-icon">⚡</div>
                <div class="segment-title">
                    <h2>East End Substation</h2>
                    <p>192.168.100.0/24 · IEC 61850</p>
                </div>
            </div>
            <div class="device" id="breaker-v1">
                <div class="device-name">Breaker IED v1 (Zone A)</div>
                <div class="device-status">● Checking...</div>
                <div class="device-data">Loading...</div>
            </div>
            <div class="device" id="breaker-v2">
                <div class="device-name">Breaker IED v2</div>
                <div class="device-status">● Checking...</div>
                <div class="device-data">Loading...</div>
            </div>
        </div>

        <div class="segment">
            <div class="segment-header">
                <div class="segment-icon">🏭</div>
                <div class="segment-title">
                    <h2>Industrial District</h2>
                    <p>192.168.200.0/24 · Modbus TCP</p>
                </div>
            </div>
            <div class="device" id="openplc">
                <div class="device-name">OpenPLC Runtime</div>
                <div class="device-status">● Checking...</div>
                <div class="device-data">Loading...</div>
            </div>
            <div class="device" id="scadabr">
                <div class="device-name">ScadaBR SCADA</div>
                <div class="device-status">● Checking...</div>
                <div class="device-data">Loading...</div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>⚠️ This monitoring station is exposed to internet - potential attack entry point</p>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def api_status():
    substation_data = {
        'breaker_v1': fetch_breaker('192.168.100.2', 9000),
        'breaker_v2': fetch_breaker('192.168.100.3', 9000)
    }
    industrial_data = {
        'openplc': fetch_openplc('192.168.200.2', 8080),
        'scadabr': fetch_scadabr('192.168.200.3', 8080)
    }
    online = sum([
        1 if substation_data['breaker_v1']['online'] else 0,
        1 if substation_data['breaker_v2']['online'] else 0,
        1 if industrial_data['openplc']['online'] else 0,
        1 if industrial_data['scadabr']['online'] else 0,
        2
    ])
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'summary': {'total_devices': 6, 'online_devices': online},
        'substation': substation_data,
        'industrial': industrial_data
    })

def fetch_breaker(ip, port):
    try:
        r = requests.get(f'http://{ip}:{port}/status', timeout=2)
        if r.status_code == 200:
            d = r.json()
            pos = 'CLOSED' if d.get('pos') == 2 else 'OPEN' if d.get('pos') == 1 else 'UNKNOWN'
            return {'online': True, 'data': f"Position: {pos} | stNum: {d.get('stNum')}"}
    except: pass
    return {'online': False, 'data': None}

def fetch_openplc(ip, port):
    try:
        r = requests.get(f'http://{ip}:{port}/', timeout=2)
        if r.status_code == 200:
            return {'online': True, 'data': f"PLC Active | Modbus: {ip}:502"}
    except: pass
    return {'online': False, 'data': None}

def fetch_scadabr(ip, port):
    try:
        r = requests.get(f'http://{ip}:{port}/ScadaBR/', timeout=2)
        if r.status_code == 200:
            return {'online': True, 'data': f"SCADA HMI Active"}
    except: pass
    return {'online': False, 'data': None}

if __name__ == '__main__':
    print("Gotham City Central Monitoring Station")
    print("Dashboard: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
