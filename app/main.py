# Main application entry point
# app/main.py
from flask import Flask

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    # Anti-clickjacking protection
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    
    # Permissions Policy
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    # Additional security headers
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Hide server information
    response.headers.pop('Server', None)
    
    return response

@app.route("/")
def index():
    return "Hello from secure-cicd-pipeline!"

if __name__ == "__main__":
    # Use environment variable for host, default to localhost for security
    import os
    host = os.environ.get('FLASK_HOST', '0.0.0.0')  # Changed for Docker compatibility
    port = int(os.environ.get('FLASK_PORT', 5001))
    app.run(host=host, port=port)
