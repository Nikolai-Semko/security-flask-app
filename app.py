#!/usr/bin/env python3
from flask import Flask
import os

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>🎉 Azure App Service Test</h1>
    <p>Application is running successfully!</p>
    <p>Environment: {}</p>
    '''.format(os.environ.get('ENV', 'Development'))

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'App is running'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)