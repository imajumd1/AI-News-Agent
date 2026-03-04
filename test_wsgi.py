"""Minimal test WSGI app for Railway debugging."""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from AI News Agent! The app is working!"

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "Railway deployment successful"})

@app.route('/test')
def test():
    return "Test endpoint works!"

if __name__ == "__main__":
    app.run()
