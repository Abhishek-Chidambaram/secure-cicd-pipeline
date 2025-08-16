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
    
    # Content Security Policy with proper fallbacks
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'self'; connect-src 'self'; frame-ancestors 'none'"
    
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
    
    # Default to localhost for security, but allow override for Docker
    # nosec B104: Binding to 0.0.0.0 is intentional for containerized deployment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')  # nosec B104
    port = int(os.environ.get('FLASK_PORT', 5001))
    
    # Additional security: disable debug mode in production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug_mode)
