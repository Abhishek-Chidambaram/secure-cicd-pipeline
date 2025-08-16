# Main application entry point
# app/main.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from secure-cicd-pipeline!"

if __name__ == "__main__":
    # Use environment variable for host, default to localhost for security
    import os
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5001))
    app.run(host=host, port=port)
