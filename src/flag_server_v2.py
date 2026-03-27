#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
from pathlib import Path

PORT = 9000
STATUS_FILE = '/tmp/breaker_status.json'
MAX_FILE_SIZE = 10240  # 10KB limit

class BreakerStatusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ['/', '/index.html', '/status']:
            self.send_response(404)
            self.end_headers()
            return

        if self.path == '/status':
            try:
                if os.path.exists(STATUS_FILE):
                    if os.path.getsize(STATUS_FILE) > MAX_FILE_SIZE:
                        raise ValueError("Status file too large")
                    with open(STATUS_FILE, 'r') as f:
                        data = json.load(f)
                    if not isinstance(data, dict):
                        raise ValueError("Invalid status format")
                    safe_data = {
                        'pos': int(data.get('pos', 0)),
                        'opCnt': int(data.get('opCnt', 0)),
                        'stNum': int(data.get('stNum', 0)),
                        'sqNum': int(data.get('sqNum', 0)),
                        'commStatus': str(data.get('commStatus', 'UNKNOWN'))[:20]
                    }
                    if safe_data['pos'] == 1:
                        safe_data['blackout'] = True
                else:
                    safe_data = {"error": "Status not available"}

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.end_headers()
                self.wfile.write(json.dumps(safe_data).encode())
            except (json.JSONDecodeError, ValueError, KeyError):
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid data"}).encode())
            except Exception:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Server error"}).encode())

        elif self.path == '/' or self.path == '/index.html':
            html = """<!DOCTYPE html>
<html>
<head>
    <title>Apex City Grid &mdash; Zone B Feeder Substation</title>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="2">
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #0d1117 100%);
            color: #ccc;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            transition: background 1s ease;
        }
        body.blackout-bg {
            background: linear-gradient(135deg, #0a0000 0%, #1a0000 100%);
        }
        .container {
            background: rgba(15, 15, 20, 0.98);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 40px rgba(0, 180, 255, 0.15);
            text-align: center;
            max-width: 680px;
            width: 100%;
            border: 1px solid #0088cc;
        }
        .header {
            background: #0f0f0f;
            padding: 18px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #222;
        }
        h1 {
            color: #00aaff;
            margin: 0;
            font-size: 22px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .subtitle {
            color: #555;
            font-size: 12px;
            margin-top: 5px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .scenario {
            background: #0d0d0d;
            border-left: 3px solid #0088cc;
            padding: 14px 16px;
            margin: 18px 0;
            text-align: left;
            font-size: 13px;
            line-height: 1.7;
            color: #999;
            border-radius: 0 6px 6px 0;
        }
        .scenario-title {
            color: #00aaff;
            font-weight: bold;
            margin-bottom: 6px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .status {
            font-size: 32px;
            font-weight: bold;
            padding: 22px;
            border-radius: 8px;
            margin: 18px 0;
            text-transform: uppercase;
            letter-spacing: 3px;
            transition: all 0.5s ease;
        }
        .energised {
            background: #0a1a0a;
            color: #00e676;
            border: 1px solid #00e676;
            box-shadow: 0 0 20px rgba(0, 230, 118, 0.2);
        }
        .tripped {
            background: #0d0000;
            color: #ff3300;
            border: 1px solid #ff3300;
            box-shadow: 0 0 40px rgba(255, 50, 0, 0.5);
            animation: flicker 3s infinite;
        }
        @keyframes flicker {
            0%, 89%, 91%, 93%, 100% { opacity: 1; }
            90%, 92% { opacity: 0.3; }
        }
        .grid-status {
            background: #0d0d0d;
            padding: 14px;
            border-radius: 6px;
            margin: 14px 0;
            border: 1px solid #1a1a1a;
            font-size: 13px;
        }
        .grid-status h3 {
            margin: 0 0 8px 0;
            color: #00aaff;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .blocked-banner {
            background: #001a00;
            border: 2px solid #00e676;
            color: #00e676;
            font-family: 'Courier New', monospace;
            font-size: 15px;
            font-weight: bold;
            padding: 16px;
            margin: 18px 0;
            border-radius: 6px;
            box-shadow: 0 0 20px rgba(0, 230, 118, 0.3);
            letter-spacing: 1px;
            line-height: 1.8;
        }
        .blackout-banner {
            background: #000;
            border: 2px solid #ff3300;
            color: #ff3300;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            font-weight: bold;
            padding: 18px;
            margin: 18px 0;
            border-radius: 6px;
            box-shadow: 0 0 40px rgba(255, 50, 0, 0.5);
            animation: pulse-red 1.5s infinite;
            letter-spacing: 1px;
            line-height: 1.8;
        }
        @keyframes pulse-red {
            0%, 100% { box-shadow: 0 0 30px rgba(255, 50, 0, 0.4); }
            50% { box-shadow: 0 0 70px rgba(255, 50, 0, 0.9); }
        }
        .info {
            background: #0d0d0d;
            padding: 18px;
            border-radius: 8px;
            margin-top: 18px;
            text-align: left;
            border: 1px solid #1a1a1a;
        }
        .info-title {
            color: #00aaff;
            font-weight: bold;
            margin-bottom: 14px;
            font-size: 11px;
            border-bottom: 1px solid #1a1a1a;
            padding-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .info div { margin: 7px 0; font-size: 13px; }
        .label { color: #555; display: inline-block; width: 200px; }
        .value { color: #ddd; font-weight: bold; }
        .hidden { display: none; }
        .badge {
            display: inline-block;
            background: #111;
            border: 1px solid #222;
            padding: 3px 9px;
            border-radius: 4px;
            font-size: 11px;
            margin: 3px;
            color: #666;
        }
        .badge.secure { border-color: #00aaff; color: #00aaff; }
    </style>
    <script>
        async function updateStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();

                const statusDiv = document.getElementById('status');
                const posDiv = document.getElementById('position');
                const opCntDiv = document.getElementById('opcount');
                const bannerDiv = document.getElementById('banner');
                const gridMsgDiv = document.getElementById('grid-msg');

                if (data.error) {
                    statusDiv.textContent = 'ERROR';
                    statusDiv.className = 'status';
                } else {
                    const pos = data.pos !== undefined ? data.pos : 2;

                    if (pos == 2) {
                        statusDiv.textContent = '\u26a1 ENERGISED';
                        statusDiv.className = 'status energised';
                        posDiv.innerHTML = '<span class="value">CLOSED (2)</span>';
                        gridMsgDiv.innerHTML = 'Zone B Feeder: <strong style="color:#00e676">ONLINE</strong> \u2014 Supplying load normally. Replay attacks blocked.';
                        bannerDiv.className = 'blocked-banner';
                        bannerDiv.innerHTML = '\u2705  REPLAY ATTACK BLOCKED  \u2705<br><span style="font-size:13px;font-weight:normal;letter-spacing:0">stNum/sqNum validation active \u2014 replayed GOOSE frames rejected</span>';
                        document.body.className = '';
                    } else if (pos == 1) {
                        statusDiv.textContent = '\u25cf BREAKER TRIPPED \u2014 BLACKOUT';
                        statusDiv.className = 'status tripped';
                        posDiv.innerHTML = '<span class="value">OPEN (1)</span>';
                        gridMsgDiv.innerHTML = 'Zone B Feeder: <strong style="color:#ff3300">DE-ENERGISED</strong> \u2014 Downstream load lost.';
                        bannerDiv.className = 'blackout-banner';
                        bannerDiv.innerHTML = '\u26a0\ufe0f  BREAKER TRIPPED  \u26a0\ufe0f<br><span style="font-size:13px;font-weight:normal;letter-spacing:0">Legitimate TRIP command received and validated</span>';
                        document.body.className = 'blackout-bg';
                    } else {
                        statusDiv.textContent = 'OPERATING...';
                        statusDiv.className = 'status';
                        posDiv.innerHTML = '<span class="value">INTERMEDIATE (0)</span>';
                        gridMsgDiv.innerHTML = 'Zone B Feeder: Breaker in transition...';
                        bannerDiv.className = 'hidden';
                        document.body.className = '';
                    }

                    opCntDiv.innerHTML = '<span class="value">' + (data.opCnt || '0') + '</span>';
                    document.getElementById('stnum').innerHTML = '<span class="value">' + (data.stNum || '0') + '</span>';
                    document.getElementById('sqnum').innerHTML = '<span class="value">' + (data.sqNum || '0') + '</span>';
                    document.getElementById('comm').innerHTML = '<span class="value">' + (data.commStatus || 'OK') + '</span>';
                }
            } catch (e) {
                document.getElementById('status').textContent = 'CONNECTION ERROR';
            }
        }

        setInterval(updateStatus, 2000);
        updateStatus();
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>&#9889; Apex City Grid</h1>
            <div class="subtitle">Zone B Feeder Substation &mdash; IED Monitor</div>
        </div>

        <div class="scenario">
            <div class="scenario-title">Demo Scenario</div>
            This substation feeds Zone B of Apex City. Unlike Zone A, this IED implements
            <strong style="color:#00aaff">IEC 61850-8-1 compliant stNum/sqNum validation</strong> &mdash;
            replayed GOOSE frames are detected and rejected. An attacker must craft a packet
            with a higher stNum than the current observed value to succeed.
        </div>

        <div id="status" class="status">LOADING...</div>

        <div class="grid-status">
            <h3>Grid Impact</h3>
            <div id="grid-msg" style="color:#666">Checking feeder status...</div>
        </div>

        <div id="banner" class="hidden"></div>

        <div class="info">
            <div class="info-title">IEC 61850 GOOSE &mdash; Live Protocol State</div>
            <div><span class="label">Breaker Position:</span> <span id="position">-</span></div>
            <div><span class="label">Operation Count:</span> <span id="opcount">-</span></div>
            <div><span class="label">State Number (stNum):</span> <span id="stnum">-</span></div>
            <div><span class="label">Sequence Number (sqNum):</span> <span id="sqnum">-</span></div>
            <div><span class="label">Communication Status:</span> <span id="comm">-</span></div>
            <div style="margin-top: 14px;">
                <span class="badge">IEC 61850-8-1</span>
                <span class="badge">GOOSE Multicast</span>
                <span class="badge secure">stNum/sqNum Validated</span>
                <span class="badge">192.168.100.0/24</span>
            </div>
        </div>
    </div>
</body>
</html>"""
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.end_headers()
            self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass

with socketserver.TCPServer(("0.0.0.0", PORT), BreakerStatusHandler) as httpd:
    print(f"Zone B Feeder IED Status Server running on port {PORT}")
    httpd.serve_forever()
