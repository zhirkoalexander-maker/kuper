"""
FPS Tester - Backend Server for System Metrics
Provides API endpoints for JavaScript frontend to get real system metrics
"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import psutil
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for JavaScript fetch requests

# Check if psutil is available
HAS_PSUTIL = True
try:
    import psutil
except ImportError:
    HAS_PSUTIL = False
    print("Warning: psutil not installed. Install with: pip install psutil")

# Store metrics history for graphs
metrics_history = {
    'cpu': [],
    'ram': [],
    'disk': [],
    'timestamps': []
}

MAX_HISTORY = 100  # Keep last 100 readings


@app.route('/api/system-metrics', methods=['GET'])
def get_system_metrics():
    """
    Get current system metrics
    
    Returns JSON:
    {
        "cpu_percent": 45.2,
        "ram_percent": 62.1,
        "ram_usage_mb": 1024,
        "ram_available_mb": 8192,
        "disk_percent": 78.5,
        "disk_free_gb": 50.2,
        "has_psutil": true,
        "timestamp": "2024-01-15T10:30:45"
    }
    """
    
    metrics = {
        "has_psutil": HAS_PSUTIL,
        "timestamp": datetime.now().isoformat()
    }
    
    if HAS_PSUTIL:
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            metrics['cpu_percent'] = cpu_percent
            
            # RAM metrics
            ram = psutil.virtual_memory()
            metrics['ram_percent'] = ram.percent
            metrics['ram_usage_mb'] = round(ram.used / 1024 / 1024, 1)
            metrics['ram_available_mb'] = round(ram.available / 1024 / 1024, 1)
            metrics['ram_total_mb'] = round(ram.total / 1024 / 1024, 1)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            metrics['disk_percent'] = disk.percent
            metrics['disk_free_gb'] = round(disk.free / 1024 / 1024 / 1024, 1)
            metrics['disk_total_gb'] = round(disk.total / 1024 / 1024 / 1024, 1)
            
            # Store in history
            if len(metrics_history['cpu']) >= MAX_HISTORY:
                metrics_history['cpu'].pop(0)
                metrics_history['ram'].pop(0)
                metrics_history['disk'].pop(0)
                metrics_history['timestamps'].pop(0)
            
            metrics_history['cpu'].append(cpu_percent)
            metrics_history['ram'].append(ram.percent)
            metrics_history['disk'].append(disk.percent)
            metrics_history['timestamps'].append(datetime.now().isoformat())
            
            metrics['status'] = 'success'
            
        except Exception as e:
            metrics['error'] = str(e)
            metrics['status'] = 'error'
            metrics['cpu_percent'] = 0
            metrics['ram_percent'] = 0
            metrics['disk_percent'] = 0
    else:
        metrics['status'] = 'psutil_not_available'
        metrics['message'] = 'psutil not installed. Install with: pip install psutil'
        metrics['cpu_percent'] = 0
        metrics['ram_percent'] = 0
        metrics['disk_percent'] = 0
    
    return jsonify(metrics)


@app.route('/api/system-metrics-history', methods=['GET'])
def get_metrics_history():
    """
    Get historical system metrics for graphs
    
    Returns JSON:
    {
        "cpu": [45.2, 48.1, 42.3, ...],
        "ram": [62.1, 63.5, 61.8, ...],
        "disk": [78.5, 78.5, 78.5, ...],
        "timestamps": ["2024-01-15T10:30:00", ...]
    }
    """
    return jsonify({
        'cpu': metrics_history['cpu'],
        'ram': metrics_history['ram'],
        'disk': metrics_history['disk'],
        'timestamps': metrics_history['timestamps']
    })


@app.route('/api/system-info', methods=['GET'])
def get_system_info():
    """
    Get static system information
    
    Returns JSON:
    {
        "processor_count": 8,
        "processor_freq_ghz": 2.4,
        "total_ram_gb": 16,
        "hostname": "my-computer",
        "os": "darwin",
        "platform": "macOS-12.5.1"
    }
    """
    
    info = {}
    
    if HAS_PSUTIL:
        try:
            info['processor_count'] = psutil.cpu_count(logical=False)
            info['processor_count_logical'] = psutil.cpu_count(logical=True)
            
            freq = psutil.cpu_freq()
            if freq:
                info['processor_freq_ghz'] = round(freq.current / 1000, 2)
            
            ram = psutil.virtual_memory()
            info['total_ram_gb'] = round(ram.total / 1024 / 1024 / 1024, 1)
            
            info['hostname'] = os.uname().nodename
            info['os'] = os.uname().sysname.lower()
            info['platform'] = f"{os.uname().sysname}-{os.uname().release}"
            
            info['status'] = 'success'
        except Exception as e:
            info['status'] = 'error'
            info['error'] = str(e)
    else:
        info['status'] = 'psutil_not_available'
    
    return jsonify(info)


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns JSON: {"status": "ok", "psutil": true}
    """
    return jsonify({
        'status': 'ok',
        'psutil': HAS_PSUTIL,
        'version': '2.0'
    })


@app.route('/', methods=['GET'])
def index():
    """
    Simple status page showing available endpoints
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FPS Tester - Backend API</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #1e1e1e; color: #fff; }
            h1 { color: #00ff00; }
            .endpoint { background: #2d2d2d; padding: 15px; margin: 10px 0; border-left: 4px solid #00ff00; }
            code { background: #000; padding: 2px 5px; }
            .status-ok { color: #00ff00; }
            .status-error { color: #ff4444; }
        </style>
    </head>
    <body>
        <h1>🎮 FPS Tester - Backend Server</h1>
        <p>System Metrics API for JavaScript Frontend</p>
        
        <h2>Status</h2>
        <p class="status-ok">✓ Server is running</p>
        <p>psutil: <span class="status-ok">✓ Installed</span></p>
        
        <h2>Available Endpoints</h2>
        
        <div class="endpoint">
            <strong>GET /api/health</strong><br>
            Health check<br>
            <code>curl http://localhost:5000/api/health</code>
        </div>
        
        <div class="endpoint">
            <strong>GET /api/system-metrics</strong><br>
            Current CPU, RAM, Disk metrics<br>
            <code>curl http://localhost:5000/api/system-metrics</code>
        </div>
        
        <div class="endpoint">
            <strong>GET /api/system-metrics-history</strong><br>
            Historical metrics for graphs<br>
            <code>curl http://localhost:5000/api/system-metrics-history</code>
        </div>
        
        <div class="endpoint">
            <strong>GET /api/system-info</strong><br>
            Static system information<br>
            <code>curl http://localhost:5000/api/system-info</code>
        </div>
        
        <h2>Example JavaScript Usage</h2>
        <pre>
// Get current metrics
fetch('/api/system-metrics')
  .then(r => r.json())
  .then(data => {
    console.log('CPU:', data.cpu_percent);
    console.log('RAM:', data.ram_percent);
    console.log('Disk:', data.disk_percent);
  });
        </pre>
        
        <hr>
        <p>FPS Tester v2.0 | Backend Server</p>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == '__main__':
    print("🎮 FPS Tester Backend Server")
    print("=" * 50)
    print(f"psutil: {'✓ Available' if HAS_PSUTIL else '✗ Not installed'}")
    print("=" * 50)
    print("Starting server on http://localhost:5000")
    print("Available endpoints:")
    print("  GET /api/health")
    print("  GET /api/system-metrics")
    print("  GET /api/system-metrics-history")
    print("  GET /api/system-info")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
