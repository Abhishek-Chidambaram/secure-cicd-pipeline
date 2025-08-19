# Main application entry point
# app/main.py
#Commit 1
import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
# This will fail silently if .env doesn't exist (which is fine for containers)
load_dotenv(verbose=False)

app = Flask(__name__)

# Configure app with secrets from environment
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')

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
    env = os.environ.get('FLASK_ENV', 'development')
    return f"Hello from secure-cicd-pipeline! Environment: {env}"

@app.route("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "environment": os.environ.get('FLASK_ENV', 'development')}

if __name__ == "__main__":
    try:
        # Default to localhost for security, but allow override for Docker
        # nosec B104: Binding to 0.0.0.0 is intentional for containerized deployment
        host = os.environ.get('FLASK_HOST', '0.0.0.0')  # nosec B104
        port = int(os.environ.get('FLASK_PORT', 5001))
        
        # Additional security: disable debug mode in production
        debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        
        print(f"Starting Flask app on {host}:{port}")
        print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
        
        app.run(host=host, port=port, debug=debug_mode)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
