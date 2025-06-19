from flask import Flask, jsonify, request, render_template_string
import logging
import json
from datetime import datetime
import os


app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# В памяти хранилище для логов
security_logs = []

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Security Lab Application</title>
    </head>
    <body>
        <h1>🔐 Security Lab Application</h1>
        <p>Application is running successfully!</p>
        <p>Environment: {{ env }}</p>
        <h2>Available Endpoints:</h2>
        <ul>
            <li><a href="/api/health">/api/health</a> - Health check</li>
            <li><a href="/api/logs">/api/logs</a> - Security logs</li>
            <li>/api/attack/sql - SQL injection simulation</li>
        </ul>
    </body>
    </html>
    ''', env=os.environ.get('ENVIRONMENT', 'Production'))

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'security-lab'
    })

@app.route('/api/logs')
def get_logs():
    return jsonify({
        'logs': security_logs,
        'count': len(security_logs)
    })

@app.route('/api/attack/sql', methods=['POST'])
def simulate_sql_injection():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        # Логируем попытку атаки
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'sql_injection_attempt',
            'query': query,
            'source_ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'Unknown')
        }
        
        security_logs.append(log_entry)
        logger.warning(f"SQL Injection attempt detected: {query}")
        
        return jsonify({
            'status': 'detected',
            'message': 'SQL injection attempt logged',
            'query': query
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))