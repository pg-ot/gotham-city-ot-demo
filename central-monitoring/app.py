from flask import Flask, jsonify, render_template_string, request
import requests
import os
import urllib.parse
from datetime import datetime

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WayneTech Operations · Central Command</title>
    <!-- Use Google Fonts JURA for scifi/tech look and Rajdhani for bold headers -->
    <link href="https://fonts.googleapis.com/css2?family=Jura:wght@400;600;700&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <style>
        :root {
            --wt-dark: #05080f;
            --wt-panel: #0a111c;
            --wt-border: #1e293b;
            --wt-blue: #0ea5e9;
            --wt-neon: #38bdf8;
            --wt-gold: #f59e0b;
            --wt-red: #ef4444;
            --wt-green: #10b981;
            --wt-text: #e2e8f0;
            --wt-muted: #64748b;
        }
        body { 
            margin: 0; font-family: 'Jura', sans-serif; 
            background: var(--wt-dark); color: var(--wt-text);
            background-image: 
                linear-gradient(rgba(14, 165, 233, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(14, 165, 233, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
            min-height: 100vh; overflow-x: hidden;
            text-shadow: 0 0 1px rgba(255,255,255,0.1);
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 2rem; }
        
        /* Header */
        .header { 
            display: flex; justify-content: space-between; align-items: center; 
            border-bottom: 2px solid var(--wt-border); 
            padding-bottom: 1.5rem; margin-bottom: 2.5rem; 
            position: relative;
        }
        .header::after {
            content: ''; position: absolute; bottom: -2px; left: 0; 
            width: 150px; height: 2px; background: var(--wt-blue);
            box-shadow: 0 0 10px var(--wt-blue);
        }
        .header h1 { 
            font-family: 'Rajdhani', sans-serif; font-size: 2.5rem; 
            font-weight: 700; margin: 0; letter-spacing: 2px;
            color: #fff; text-shadow: 0 0 15px rgba(14, 165, 233, 0.4);
        }
        .header h1 span { color: var(--wt-blue); }
        .live-status { 
            display: flex; align-items: center; gap: 0.75rem; 
            font-size: 1.1rem; color: var(--wt-neon); font-weight: 600; 
            text-transform: uppercase; letter-spacing: 2px;
            padding: 8px 16px; border: 1px solid rgba(14, 165, 233, 0.2);
            border-radius: 4px; background: rgba(14, 165, 233, 0.05);
            box-shadow: inset 0 0 15px rgba(14, 165, 233, 0.1);
        }
        .pulse { 
            width: 12px; height: 12px; background: var(--wt-green); 
            border-radius: 50%; box-shadow: 0 0 12px var(--wt-green); 
            animation: pulse-anim 2s infinite; 
        }
        @keyframes pulse-anim { 
            0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.8); } 
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); } 
            100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } 
        }

        /* Layout */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; }
        @media(max-width: 1000px){ .grid { grid-template-columns: 1fr; } }
        
        /* Panels */
        .panel { 
            background: var(--wt-panel); border: 1px solid var(--wt-border); 
            border-radius: 12px; padding: 2.5rem; position: relative; 
            box-shadow: inset 0 0 60px rgba(0,0,0,0.8), 0 20px 40px rgba(0,0,0,0.4);
        }
        .panel::before {
            content: 'BAT-OS VER 9.2 // PROTOCOL ACTIVE'; position: absolute; top: 12px; right: 20px;
            font-size: 10px; color: var(--wt-muted); letter-spacing: 2px; opacity: 0.5;
            font-family: 'Courier New', monospace;
        }
        
        .panel-header { 
            display: flex; flex-direction: column; margin-bottom: 2rem; 
            border-left: 4px solid var(--wt-blue); padding-left: 1.25rem;
        }
        .industrial .panel-header { border-left-color: var(--wt-gold); }
        .panel-header h2 { 
            font-family: 'Rajdhani', sans-serif; font-size: 2.2rem; 
            font-weight: 700; margin: 0; color: #fff; text-transform: uppercase;
            letter-spacing: 1px;
        }
        .panel-header p { 
            margin: 5px 0 0 0; color: var(--wt-muted); 
            font-size: 0.95rem; letter-spacing: 1.5px;
        }
        
        /* ECharts Containers */
        .dials-container { display: flex; gap: 1.5rem; margin-bottom: 2.5rem; }
        .chart-box { 
            flex: 1; height: 300px; 
            background: linear-gradient(180deg, rgba(30,41,59,0.3) 0%, rgba(0,0,0,0.5) 100%);
            border: 1px solid rgba(255,255,255,0.03);
            border-radius: 8px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        }

        /* Device Lists */
        h3.section-header { 
            margin-top: 2rem; padding-bottom: 10px; border-bottom: 1px solid var(--wt-border);
            font-size: 1.1rem; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 2px; 
            display: flex; align-items: center; gap: 10px;
        }
        h3.section-header::before { content: '■'; color: var(--wt-blue); font-size: 0.8rem; }
        .industrial h3.section-header::before { color: var(--wt-gold); }

        .devices-list { display: flex; flex-direction: column; gap: 1rem; }
        
        .device-card { 
            display: flex; justify-content: space-between; align-items: center; 
            background: linear-gradient(90deg, rgba(30,41,59,0.5), transparent); 
            padding: 1.25rem 1.5rem; border-radius: 6px; 
            border-left: 3px solid var(--wt-border);
            transition: all 0.3s ease; cursor: default;
        }
        .device-card:hover { 
            background: linear-gradient(90deg, rgba(30,41,59,0.9), rgba(0,0,0,0.3)); 
            border-left-color: var(--wt-neon); transform: translateX(5px);
        }
        .industrial .device-card:hover { border-left-color: var(--wt-gold); }
        .device-card.offline { opacity: 0.4; border-left-color: var(--wt-red) !important; filter: grayscale(100%); }
        
        .d-info h4 { margin: 0 0 8px 0; font-size: 1.2rem; font-family: 'Rajdhani', sans-serif; color: #fff; letter-spacing: 1px; }
        .d-info p { margin: 0; font-size: 0.95rem; color: var(--wt-neon); font-family: 'Courier New', monospace; opacity: 0.9;}
        .industrial .d-info p { color: var(--wt-gold); }

        .d-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
        .badge { 
            font-size: 0.75rem; padding: 4px 8px; border-radius: 4px; 
            background: rgba(0,0,0,0.5); color: #94a3b8; 
            border: 1px solid rgba(255,255,255,0.1);
            font-family: 'Courier New', monospace; font-weight: 600;
        }
        
        .status-badge { 
            font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; font-weight: 700; 
            color: var(--wt-green); text-transform: uppercase; letter-spacing: 2px; 
            display: flex; align-items: center; gap: 8px;
            text-shadow: 0 0 10px rgba(16,185,129,0.5);
        }
        .status-badge::before { content: ''; display: block; width: 8px; height: 8px; background: var(--wt-green); border-radius: 50%; box-shadow: 0 0 10px var(--wt-green); }
        .offline .status-badge { color: var(--wt-red); text-shadow: 0 0 10px rgba(239,68,68,0.5); }
        .offline .status-badge::before { background: var(--wt-red); box-shadow: 0 0 10px var(--wt-red); }
        
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>WAYNE<span>TECH</span> CENTRAL COMMAND</h1>
            <div class="live-status"><div class="pulse"></div> SECURE SESSION</div>
        </header>

        <div class="grid">
            <!-- SUBSTATION -->
            <div class="panel substation">
                <div class="panel-header">
                    <h2>⚡ East End Substation</h2>
                    <p>CAPACITY: 42,000 RESIDENTS | SECURE RING</p>
                </div>
                
                <div class="dials-container">
                    <div id="gauge-voltage" class="chart-box"></div>
                    <div id="gauge-freq" class="chart-box"></div>
                </div>
                
                <h3 class="section-header">Infrastructure Topography</h3>
                <div class="devices-list" id="substation-devices">
                    <div class="device-card offline"><div class="d-info"><h4>Connecting...</h4><p>Establishing link</p></div></div>
                </div>
            </div>

            <!-- INDUSTRIAL -->
            <div class="panel industrial">
                <div class="panel-header">
                    <h2>🏭 Wayne Enterprises</h2>
                    <p>INDUSTRIAL DISTRICT | EXPERIMENTAL FABRICATION</p>
                </div>
                
                <div class="dials-container">
                    <div id="gauge-temp" class="chart-box"></div>
                    <div id="gauge-pressure" class="chart-box"></div>
                </div>
                
                <h3 class="section-header">Process Automation Nodes</h3>
                <div class="devices-list" id="industrial-devices">
                    <div class="device-card offline"><div class="d-info"><h4>Connecting...</h4><p>Establishing link</p></div></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ECharts Configs using Dark Cyberpunk / Industrial Themes
        const darkGauge = {
            type: 'gauge',
            startAngle: 210, endAngle: -30,
            splitNumber: 5,
            axisLine: { lineStyle: { width: 14, color: [[1, 'rgba(255,255,255,0.05)']] } },
            progress: { show: true, width: 14 },
            pointer: { icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z', length: '65%', width: 8, offsetCenter: [0, '-10%'], itemStyle: { color: '#fff', shadowBlur: 10, shadowColor: 'rgba(255,255,255,0.5)' } },
            axisTick: { distance: -24, length: 10, lineStyle: { color: 'rgba(255,255,255,0.2)', width: 1 } },
            splitLine: { distance: -30, length: 16, lineStyle: { color: 'rgba(255,255,255,0.5)', width: 2 } },
            axisLabel: { distance: -15, color: '#64748b', fontSize: 11, fontFamily: 'Jura', fontWeight: 600 },
            anchor: { show: true, showAbove: true, size: 20, itemStyle: { borderWidth: 5 } },
            title: { show: true, offsetCenter: [0, '40%'], color: '#94a3b8', fontSize: 13, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 2 },
            detail: { valueAnimation: true, fontSize: 26, fontWeight: 700, color: '#fff', offsetCenter: [0, '70%'], textShadowBlur: 10, formatter: '{value}' }
        };

        const blueTheme = { 
            color: '#0ea5e9', shadowColor: 'rgba(14,165,233,0.6)', shadowBlur: 15 
        };
        const goldTheme = { 
            color: '#f59e0b', shadowColor: 'rgba(245,158,11,0.6)', shadowBlur: 15 
        };

        // Initialize ECharts instances
        const cVolt = echarts.init(document.getElementById('gauge-voltage'));
        cVolt.setOption({ series: [{ ...darkGauge, min: 100, max: 130, itemStyle: blueTheme, anchor: { ...darkGauge.anchor, itemStyle: { borderColor: blueTheme.color } }, detail: { ...darkGauge.detail, formatter: '{value} kV', textShadowColor: blueTheme.color }, data: [{ value: 115.2, name: 'GRID VOLTAGE' }] }] });

        const cFreq = echarts.init(document.getElementById('gauge-freq'));
        cFreq.setOption({ series: [{ ...darkGauge, min: 58, max: 62, itemStyle: blueTheme, anchor: { ...darkGauge.anchor, itemStyle: { borderColor: blueTheme.color } }, detail: { ...darkGauge.detail, formatter: '{value} Hz', textShadowColor: blueTheme.color }, data: [{ value: 60.01, name: 'FREQUENCY' }] }] });

        const cTemp = echarts.init(document.getElementById('gauge-temp'));
        cTemp.setOption({ series: [{ ...darkGauge, min: 200, max: 800, itemStyle: goldTheme, anchor: { ...darkGauge.anchor, itemStyle: { borderColor: goldTheme.color } }, detail: { ...darkGauge.detail, formatter: '{value} °C', textShadowColor: goldTheme.color }, data: [{ value: 485, name: 'CORE TEMP' }] }] });

        const cPres = echarts.init(document.getElementById('gauge-pressure'));
        cPres.setOption({ series: [{ ...darkGauge, min: 0, max: 2000, itemStyle: goldTheme, anchor: { ...darkGauge.anchor, itemStyle: { borderColor: goldTheme.color } }, detail: { ...darkGauge.detail, formatter: '{value} PSI', textShadowColor: goldTheme.color }, data: [{ value: 1240, name: 'LINE PRESSURE' }] }] });

        window.addEventListener('resize', () => { cVolt.resize(); cFreq.resize(); cTemp.resize(); cPres.resize(); });

        // Physics-based jitter
        setInterval(() => {
            const v = (115.0 + Math.random() * 0.5).toFixed(1);
            cVolt.setOption({ series: [{ data: [{ value: v, name: 'GRID VOLTAGE' }] }] });
            const f = (60.00 + (Math.random() * 0.04 - 0.02)).toFixed(2);
            cFreq.setOption({ series: [{ data: [{ value: f, name: 'FREQUENCY' }] }] });
            const t = (485.0 + (Math.random() * 6 - 3)).toFixed(1);
            cTemp.setOption({ series: [{ data: [{ value: t, name: 'CORE TEMP' }] }] });
            const p = Math.floor(1240 + (Math.random() * 30 - 15));
            cPres.setOption({ series: [{ data: [{ value: p, name: 'LINE PRESSURE' }] }] });
        }, 1200);

        // Fetch API Data
        async function fetchData() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                // Purely named metadata based on prompt requirements
                const subMeta = {
                    'control': { id: 'CTRL-NODE-ALPHA', tags: [] },
                    'v1': { id: 'PROT-RELAY-A1', tags: ['Feeder 1', '🏙️ The Narrows', '🏙️ Crime Alley'] },
                    'v2': { id: 'PROT-RELAY-B2', tags: ['Feeder 2', '🏙️ Diamond Dist.', '🏙️ Bristol'] }
                };
                
                const indMeta = {
                    'scada': { id: 'HMI-RACK-01', tags: [] },
                    'plc': { id: 'IND-PLC-CORE', tags: ['Applied Sciences Div.'] }
                };

                // Use the exact names from user prompt
                let subHtml = `
                    ${renderCard('Control IED', subMeta.control, data.substation.control)}
                    ${renderCard('Breaker IED v1', subMeta.v1, data.substation.breaker_v1)}
                    ${renderCard('Breaker IED v2', subMeta.v2, data.substation.breaker_v2)}
                `;
                document.getElementById('substation-devices').innerHTML = subHtml;
                
                let indHtml = `
                    ${renderCard('WayneTech SCADA HMI', indMeta.scada, data.industrial.scadabr)}
                    ${renderCard('OpenPLC Runtime', indMeta.plc, data.industrial.openplc)}
                `;
                document.getElementById('industrial-devices').innerHTML = indHtml;
                
            } catch (error) {
                console.error('API Error:', error);
            }
        }
        
        function renderCard(name, meta, deviceObj) {
            const isOnline = deviceObj && deviceObj.online;
            const cls = isOnline ? '' : 'offline';
            const statusTxt = isOnline ? 'ONLINE' : 'OFFLINE';
            const dataTxt = deviceObj && deviceObj.data ? deviceObj.data : 'SIGNAL LOST';
            
            let badges = `<span class="badge">${meta.id}</span>`;
            if (meta.tags) {
                meta.tags.forEach(t => badges += `<span class="badge">${t}</span>`);
            }
            
            return `
            <div class="device-card ${cls}">
                <div class="d-info">
                    <h4>${name}</h4>
                    <p>${dataTxt}</p>
                    <div class="d-meta">${badges}</div>
                </div>
                <div class="status-badge">${statusTxt}</div>
            </div>`;
        }

        setInterval(fetchData, 3000);
        fetchData();
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def api_status():
    substation_data = {
        'control': fetch_control(),
        'breaker_v1': fetch_breaker('substation-breaker-v1'),
        'breaker_v2': fetch_breaker('substation-breaker-v2')
    }
    industrial_data = {
        'openplc': fetch_openplc('openplc'),
        'scadabr': fetch_scadabr('scadabr')
    }
    
    # Intentional SSRF Flaw
    # If the user provides a direct ?node_url= query, the backend fetches it blindly
    custom_node_url = request.args.get('node_url')
    custom_data = None
    if custom_node_url:
        try:
            r = requests.get(custom_node_url, timeout=2)
            custom_data = {'online': True, 'http_status': r.status_code, 'data': r.text[:200]}
        except Exception as e:
            custom_data = {'online': False, 'error': str(e)}
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'substation': substation_data,
        'industrial': industrial_data,
        'custom_node': custom_data
    })

@app.route('/api/diag')
def api_diag():
    # Intentional Command Injection Flaw
    # e.g., /api/diag?ip=127.0.0.1;id
    ip = request.args.get('ip', '127.0.0.1')
    try:
        # Use os.popen to execute the ping command directly against the OS
        output = os.popen(f"ping -c 1 {ip}").read()
        return jsonify({'status': 'success', 'output': output})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def fetch_control():
    # Implicitly active since it's the core control node
    return {'online': True, 'data': 'STATUS: PUBLISHER ACTIVE'}

def fetch_breaker(container_name):
    try:
        r = requests.get(f'http://{container_name}:9000/status', timeout=2)
        if r.status_code == 200:
            d = r.json()
            pos = 'CLOSED' if d.get('pos') == 2 else 'OPEN' if d.get('pos') == 1 else 'UNKNOWN'
            return {'online': True, 'data': f"STATUS: CIRCUIT {pos}"}
    except: pass
    return {'online': False, 'data': None}

def fetch_openplc(container_name):
    try:
        r = requests.get(f'http://{container_name}:8080/', timeout=2)
        if r.status_code == 200:
            # Using specific logic from prompt context, "Experimental Fabrication"
            return {'online': True, 'data': "STATUS: FABRICATION NOMINAL"}
    except: pass
    return {'online': False, 'data': None}

def fetch_scadabr(container_name):
    try:
        r = requests.get(f'http://{container_name}:8080/ScadaBR/', timeout=2)
        if r.status_code == 200:
            return {'online': True, 'data': "STATUS: VISUALIZATION PROCESS ACTIVE"}
    except: pass
    return {'online': False, 'data': None}

if __name__ == '__main__':
    print("WayneTech Central Operations Station Started")
    app.run(host='0.0.0.0', port=5000, debug=False)
