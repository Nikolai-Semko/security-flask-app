from flask import Flask, request, jsonify
import logging
import datetime
import json
from werkzeug.security import check_password_hash, generate_password_hash

# Flask application setup
app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Simple user database (use a real database in production)
users_db = {
    "admin": generate_password_hash("password123"),
    "user1": generate_password_hash("mypassword"),
    "testuser": generate_password_hash("testpass")
}

@app.route('/')
def home():
    """Home page"""
    return jsonify({
        "message": "Security Demo Flask App",
        "endpoints": {
            "/login": "POST - User authentication",
            "/health": "GET - Application health check"
        }
    })

@app.route('/health')
def health_check():
    """Application health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/login', methods=['POST'])
def login():
    """
    User authentication endpoint
    Logs all login attempts for security analysis
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            log_event = {
                "event": "login_attempt",
                "result": "failed",
                "reason": "missing_request_body",
                "ip_address": request.remote_addr,
                "user_agent": request.headers.get('User-Agent', 'Unknown'),
                "timestamp": datetime.datetime.now().isoformat()
            }
            logger.warning(f"LOGIN_FAILED: {json.dumps(log_event)}")
            return jsonify({"error": "Missing request body"}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        # Check required fields
        if not username or not password:
            log_event = {
                "event": "login_attempt",
                "result": "failed",
                "reason": "missing_credentials",
                "username": username or "not_provided",
                "ip_address": request.remote_addr,
                "user_agent": request.headers.get('User-Agent', 'Unknown'),
                "timestamp": datetime.datetime.now().isoformat()
            }
            logger.warning(f"LOGIN_FAILED: {json.dumps(log_event)}")
            return jsonify({"error": "Missing username or password"}), 400
        
        # Check user existence and password validity
        if username in users_db and check_password_hash(users_db[username], password):
            # Successful authentication
            log_event = {
                "event": "login_attempt",
                "result": "success",
                "username": username,
                "ip_address": request.remote_addr,
                "user_agent": request.headers.get('User-Agent', 'Unknown'),
                "timestamp": datetime.datetime.now().isoformat()
            }
            logger.info(f"LOGIN_SUCCESS: {json.dumps(log_event)}")
            
            return jsonify({
                "message": "Authentication successful",
                "username": username,
                "timestamp": datetime.datetime.now().isoformat()
            }), 200
        else:
            # Failed authentication
            log_event = {
                "event": "login_attempt",
                "result": "failed",
                "reason": "invalid_credentials",
                "username": username,
                "ip_address": request.remote_addr,
                "user_agent": request.headers.get('User-Agent', 'Unknown'),
                "timestamp": datetime.datetime.now().isoformat()
            }
            logger.warning(f"LOGIN_FAILED: {json.dumps(log_event)}")
            
            return jsonify({"error": "Invalid username or password"}), 401
            
    except Exception as e:
        # Log system errors
        log_event = {
            "event": "login_attempt",
            "result": "error",
            "reason": "system_error",
            "error": str(e),
            "ip_address": request.remote_addr,
            "user_agent": request.headers.get('User-Agent', 'Unknown'),
            "timestamp": datetime.datetime.now().isoformat()
        }
        logger.error(f"LOGIN_ERROR: {json.dumps(log_event)}")
        
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Run application in development mode
    app.run(debug=True, host='0.0.0.0', port=8000)