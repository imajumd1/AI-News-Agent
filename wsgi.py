"""WSGI entry point for gunicorn."""

from app import app

# Railway deployment

if __name__ == "__main__":
    app.run()
