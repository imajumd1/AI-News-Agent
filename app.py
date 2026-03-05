#!/usr/bin/env python3
"""Web application for AI News Agent."""

import sys
import os
import traceback

# Add startup logging
print("=" * 80)
print("AI News Agent - Starting Application")
print("=" * 80)
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

try:
    from flask import Flask, render_template_string, request, jsonify
    print("✓ Flask imported successfully")
except Exception as e:
    print(f"✗ Failed to import Flask: {e}")
    sys.exit(1)

try:
    from flask_mail import Mail, Message
    print("✓ Flask-Mail imported successfully")
except Exception as e:
    print(f"✗ Failed to import Flask-Mail: {e}")
    sys.exit(1)

import json
from datetime import datetime
import html
import csv

# Initialize SendGrid availability flag
SENDGRID_AVAILABLE = False

try:
    from config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM
    print("✓ Config imported successfully")
    
    # Try to import SendGrid
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail as SendGridMail, Email, To, Content
        SENDGRID_AVAILABLE = True
        print("✓ SendGrid library available")
    except ImportError:
        SENDGRID_AVAILABLE = False
        print("⚠ SendGrid library not available")
except Exception as e:
    print(f"✗ Failed to import config: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from agent import AINewsAgent
    print("✓ AINewsAgent imported successfully")
except Exception as e:
    print(f"✗ Failed to import AINewsAgent: {e}")
    traceback.print_exc()
    sys.exit(1)

print("=" * 80)
print("All imports successful - Starting Flask app")
print("=" * 80)

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

print("Creating Flask app...")
print(f"MAIL_SERVER: {MAIL_SERVER}")
print(f"MAIL_USERNAME configured: {'Yes' if MAIL_USERNAME else 'No'}")

# Configure Flask-Mail
try:
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = MAIL_USERNAME or ''
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD or ''
    mail = Mail(app)
    print("✓ Flask-Mail configured successfully")
except Exception as e:
    print(f"✗ Flask-Mail configuration failed: {e}")
    traceback.print_exc()
    # Create a dummy mail object to prevent crashes
    mail = None

# Add global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    """Log all unhandled exceptions."""
    print(f"!!! UNHANDLED EXCEPTION: {type(e).__name__}: {str(e)}")
    traceback.print_exc()
    import sys
    sys.stdout.flush()
    return f"Internal Server Error: {str(e)}", 500

print("✓ Error handlers registered")

# Enable CORS manually (for localhost, CORS isn't strictly needed, but helps)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Category configuration with icons and colors  
CATEGORY_CONFIG = {
    "GPU and AI Infra": {
        "icon": "⚙️",  # Gear for infrastructure/systems
        "color": "#667eea",
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    "AI Applications": {
        "icon": "✨",  # Sparkles for AI magic/applications
        "color": "#4facfe",
        "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
    },
    "AI Builder tools": {
        "icon": "🔨",  # Hammer for building/construction
        "color": "#f093fb",
        "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    },
    "AI startups to watch": {
        "icon": "🚀",  # Rocket for startups launching
        "color": "#fa709a",
        "gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
    }
}

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Agent</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0f;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.15) 0%, transparent 50%),
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px);
            min-height: 100vh;
            padding: 20px;
            color: #ffffff;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 40px;
            position: relative;
        }
        
        /* Ensure proper text sizing on mobile */
        html {
            -webkit-text-size-adjust: 100%;
            -moz-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }
        .header {
            background: #0a0e1a;
            border: 1px solid rgba(139, 132, 255, 0.2);
            padding: 60px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            margin-bottom: 40px;
            position: relative;
            overflow: visible;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 10% 20%, rgba(139, 132, 255, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%);
            z-index: 0;
            border-radius: 24px;
        }
        .hero-left {
            position: relative;
            z-index: 2;
            text-align: left;
        }
        .hero-badge {
            display: inline-block;
            padding: 8px 16px;
            background: rgba(139, 132, 255, 0.15);
            border: 1px solid rgba(139, 132, 255, 0.3);
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: #8b84ff;
            letter-spacing: 2px;
            margin-bottom: 35px;
            text-transform: uppercase;
        }
        .header h1 {
            color: transparent;
            background: linear-gradient(135deg, #a9a3ff 0%, #d4b3ff 100%);
            -webkit-background-clip: text;
            background-clip: text;
            margin-bottom: 25px;
            font-size: 5.5em;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -3px;
            font-family: 'Space Grotesk', sans-serif;
        }
        .header-subtitle {
            color: #b4b4c8;
            font-size: 1.5em;
            line-height: 1.4;
            margin-bottom: 45px;
            font-weight: 400;
            letter-spacing: -0.5px;
        }
        .header-tagline {
            color: #8a8a9e;
            font-size: 1.15em;
            line-height: 1.9;
            margin-bottom: 25px;
            font-weight: 400;
            letter-spacing: 0.2px;
        }
        .header-tagline:last-of-type {
            margin-bottom: 0;
        }
        .header-tagline .highlight {
            color: #d1d5db;
            font-weight: 500;
        }
        .hero-buttons {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .btn-hero {
            padding: 14px 28px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 15px;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-hero-primary {
            background: linear-gradient(135deg, #4fffb0 0%, #3b82f6 100%);
            color: #0a0e1a;
            box-shadow: 0 4px 20px rgba(79, 255, 176, 0.3);
        }
        .btn-hero-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(79, 255, 176, 0.4);
        }
        .btn-hero-secondary {
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .btn-hero-secondary:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
        }
        .hero-right {
            position: relative;
            z-index: 2;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .hero-character-container {
            position: relative;
            width: 350px;
            height: 480px;
        }
        .anya-character {
            width: 100%;
            height: 100%;
            position: relative;
            margin: 0 auto;
            animation: gentle-float 6s ease-in-out infinite;
            filter: drop-shadow(0 20px 60px rgba(124,106,255,0.4));
        }
        @keyframes gentle-float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-14px); }
        }
        .cursor-blink {
            animation: blink 1.1s step-end infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        .screen-glow {
            animation: screenFlicker 4s ease-in-out infinite;
        }
        @keyframes screenFlicker {
            0%, 100% { opacity: 1; }
            45% { opacity: 0.85; }
            50% { opacity: 1; }
            90% { opacity: 0.9; }
        }
        /* Tablet and below */
        @media (max-width: 1024px) {
            .header {
                grid-template-columns: 1fr;
                gap: 40px;
                padding: 40px 30px;
            }
            .hero-left {
                text-align: center;
            }
            .header h1 {
                font-size: 4em;
            }
            .header-subtitle {
                font-size: 1.3em;
            }
            .header-tagline {
                font-size: 1.05em;
            }
            .hero-character-container {
                width: 320px;
                height: 400px;
            }
        }
        
        /* Mobile */
        @media (max-width: 768px) {
            .container {
                padding: 20px;
                max-width: 100%;
            }
            .header {
                grid-template-columns: 1fr;
                gap: 30px;
                padding: 30px 20px;
                border-radius: 16px;
            }
            .hero-left {
                text-align: center;
            }
            .hero-badge {
                font-size: 10px;
                padding: 6px 12px;
                margin-bottom: 20px;
            }
            .header h1 {
                font-size: 3em;
                letter-spacing: -2px;
                margin-bottom: 15px;
            }
            .header-subtitle {
                font-size: 1.1em;
                margin-bottom: 25px;
            }
            .header-tagline {
                font-size: 0.95em;
                line-height: 1.7;
                margin-bottom: 15px;
            }
            .hero-character-container {
                width: 280px;
                height: 360px;
                margin: 0 auto;
            }
            .anya-character {
                width: 100%;
                height: 100%;
            }
            .controls {
                padding: 20px;
                flex-direction: column;
                gap: 15px;
            }
            .form-group {
                min-width: 100%;
            }
            .btn {
                width: 100%;
                padding: 16px;
                font-size: 16px;
            }
            .categories-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            .category-box {
                padding: 25px;
            }
            .email-section {
                padding: 20px;
                margin-top: 30px;
            }
            .email-form {
                flex-direction: column;
            }
            .email-input {
                width: 100%;
            }
            .email-send-btn {
                width: 100%;
            }
            .modal-content {
                width: 95%;
                padding: 30px 20px;
            }
            .feedback-float-btn {
                top: 20px;
                right: 40px;
                padding: 12px 20px;
                font-size: 14px;
            }
        }
        
        /* Small mobile */
        @media (max-width: 480px) {
            .header h1 {
                font-size: 2.5em;
            }
            .header-subtitle {
                font-size: 1em;
            }
            .header-tagline {
                font-size: 0.9em;
            }
            .hero-character-container {
                width: 240px;
                height: 310px;
            }
        }
        .controls {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            margin-bottom: 40px;
            display: flex;
            gap: 20px;
            align-items: flex-end;
            flex-wrap: wrap;
        }
        .form-group {
            flex: 1;
            min-width: 200px;
        }
        .form-group label {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
            color: #b4b4c8;
            font-weight: 600;
            font-size: 14px;
        }
        .form-group label::before {
            font-size: 18px;
        }
        .form-group.days-group label::before {
            content: '📅';
        }
        .form-group.mode-group label::before {
            content: '⚙️';
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 14px 18px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            font-size: 15px;
            color: #ffffff;
            transition: all 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        }
        .form-group select option {
            background: #1a1a24;
            color: #ffffff;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 40px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            white-space: nowrap;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            position: relative;
            overflow: hidden;
        }
        .btn::before {
            content: '🚀 ';
            margin-right: 8px;
        }
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6), 0 0 30px rgba(102, 126, 234, 0.4);
        }
        .btn:active {
            transform: translateY(-1px);
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 60px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 40px;
            color: #ffffff;
        }
        .spinner {
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .categories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        .category-box {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        .category-box:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.4), 0 0 40px rgba(102, 126, 234, 0.3);
            border-color: currentColor;
        }
        .category-box.expanded {
            border-color: currentColor;
            box-shadow: 0 20px 50px rgba(0,0,0,0.4), 0 0 50px currentColor;
        }
        .category-header {
            padding: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .category-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            opacity: 0.1;
            background: currentColor;
        }
        .category-icon {
            font-size: 0;
            margin-bottom: 15px;
            position: relative;
            z-index: 1;
            width: 100px;
            height: 100px;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
            background-size: cover;
            background-position: center;
            border-radius: 24px;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.3s;
            overflow: hidden;
        }
        .category-icon::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.5) 100%);
            z-index: 1;
        }
        .category-box:hover .category-icon {
            transform: scale(1.05);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        }
        /* Custom backgrounds for each category with Pexels images */
        .category-box[data-category="GPU and AI Infra"] .category-icon {
            background: 
                linear-gradient(135deg, rgba(102, 126, 234, 0.4) 0%, rgba(118, 75, 162, 0.4) 100%),
                url('https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?auto=compress&cs=tinysrgb&w=400') center/cover;
        }
        .category-box[data-category="AI Applications"] .category-icon {
            background: 
                linear-gradient(135deg, rgba(79, 172, 254, 0.4) 0%, rgba(0, 242, 254, 0.4) 100%),
                url('https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&w=400') center/cover;
        }
        .category-box[data-category="AI Builder tools"] .category-icon {
            background: 
                linear-gradient(135deg, rgba(240, 147, 251, 0.4) 0%, rgba(245, 87, 108, 0.4) 100%),
                url('https://images.pexels.com/photos/270348/pexels-photo-270348.jpeg?auto=compress&cs=tinysrgb&w=400') center/cover;
        }
        .category-box[data-category="AI startups to watch"] .category-icon {
            background: 
                linear-gradient(135deg, rgba(250, 112, 154, 0.4) 0%, rgba(254, 225, 64, 0.4) 100%),
                url('https://images.pexels.com/photos/60132/pexels-photo-60132.jpeg?auto=compress&cs=tinysrgb&w=400') center/cover;
        }
        .category-title {
            font-size: 1.4em;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }
        .category-count {
            font-size: 0.95em;
            color: #b4b4c8;
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            font-weight: 600;
        }
        .category-count::before {
            content: '●';
            font-size: 12px;
        }
        .category-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.5s ease-out;
        }
        .category-box.expanded .category-content {
            max-height: 5000px;
            transition: max-height 0.5s ease-in;
        }
        .category-overview {
            padding: 30px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            border-radius: 15px;
            margin-bottom: 25px;
            border-left: 5px solid;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .category-overview-title {
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 20px;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .category-overview-text {
            line-height: 1.8;
            color: #e0e0e8;
            font-size: 1.05em;
            font-weight: 400;
        }
        .read-more-link {
            color: #667eea;
            cursor: pointer;
            text-decoration: underline;
            font-weight: 600;
            margin-left: 5px;
        }
        .read-more-link:hover {
            color: #5568d3;
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.5);
        }
        .modal-content {
            background: linear-gradient(135deg, rgba(26, 26, 36, 0.98) 0%, rgba(18, 18, 28, 0.98) 100%);
            backdrop-filter: blur(20px);
            margin: 5% auto;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            width: 80%;
            max-width: 700px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }
        .modal-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #ffffff;
        }
        .close-modal {
            color: #8a8a9e;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            line-height: 1;
            transition: color 0.3s;
        }
        .close-modal:hover,
        .close-modal:focus {
            color: #ffffff;
        }
        .modal-body {
            line-height: 1.8;
            color: #e0e0e8;
            font-size: 1.05em;
        }
        .articles-section {
            margin-top: 20px;
        }
        .articles-toggle {
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        .articles-toggle:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: currentColor;
        }
        .articles-toggle-title {
            font-weight: 600;
            color: #ffffff;
        }
        .articles-toggle-icon {
            transition: transform 0.3s;
        }
        .articles-toggle.expanded .articles-toggle-icon {
            transform: rotate(180deg);
        }
        .articles-container {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease-out;
        }
        .articles-toggle.expanded + .articles-container {
            max-height: 10000px;
            transition: max-height 0.4s ease-in;
        }
        .articles-section {
            border-top: 2px solid #e0e0e0;
            padding-top: 20px;
        }
        .articles-list {
            padding: 20px;
        }
        .article-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 16px;
            border-left: 4px solid;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid;
            transition: all 0.3s;
        }
        .article-card:hover {
            transform: translateX(8px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            background: rgba(255, 255, 255, 0.08);
        }
        .article-title {
            font-size: 1.1em;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
            line-height: 1.5;
        }
        .article-title a {
            color: #ffffff;
            text-decoration: none;
            transition: color 0.3s;
        }
        .article-title a:hover {
            color: #667eea;
            text-decoration: none;
        }
        .article-meta {
            color: #8a8a9e;
            font-size: 0.85em;
            margin-bottom: 12px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .article-summary {
            color: #b4b4c8;
            line-height: 1.8;
            margin-bottom: 15px;
            font-size: 0.95em;
        }
        .read-more {
            display: inline-block;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9em;
            transition: all 0.3s;
        }
        .read-more:hover {
            color: #764ba2;
            transform: translateX(3px);
        }
        .read-more::after {
            content: ' →';
            transition: transform 0.3s;
        }
        .read-more:hover::after {
            transform: translateX(3px);
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #8a8a9e;
        }
        .error {
            background: rgba(244, 67, 54, 0.15);
            color: #f44336;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 4px solid #f44336;
            border: 1px solid rgba(244, 67, 54, 0.3);
        }
        .results {
            display: none;
        }
        .results.visible {
            display: block;
        }
        /* Modal Styles */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            z-index: 9999;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        }
        .modal-overlay.active {
            display: flex;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .modal-content {
            background: linear-gradient(135deg, rgba(10, 10, 15, 0.95) 0%, rgba(26, 31, 58, 0.95) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(139, 132, 255, 0.3);
            border-radius: 24px;
            padding: 40px;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 100px rgba(102, 126, 234, 0.3);
            position: relative;
            animation: slideUp 0.4s ease;
        }
        @keyframes slideUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .modal-close {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 20px;
            color: #ffffff;
            transition: all 0.3s;
        }
        .modal-close:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: rotate(90deg);
        }
        .email-section {
            margin-top: 40px;
            padding: 30px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            animation: slideIn 0.5s ease;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .email-title {
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 20px;
            color: #ffffff;
        }
        .email-form {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
        }
        .email-input {
            flex: 1;
            padding: 14px 20px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            font-size: 1em;
            transition: all 0.3s;
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
        }
        .email-input::placeholder {
            color: #8a8a9e;
        }
        .email-input:focus {
            outline: none;
            border-color: #667eea;
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        }
        .email-send-btn {
            padding: 14px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        .email-send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
        }
        .email-send-btn:disabled {
            background: rgba(255, 255, 255, 0.1);
            color: #8a8a9e;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .email-message {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            display: none;
        }
        .email-message.success {
            background: rgba(76, 175, 80, 0.2);
            color: #4caf50;
            border: 1px solid rgba(76, 175, 80, 0.4);
        }
        .email-message.error {
            background: rgba(244, 67, 54, 0.2);
            color: #f44336;
            border: 1px solid rgba(244, 67, 54, 0.4);
        }
        .feedback-section {
            padding: 0;
            background: none;
            backdrop-filter: none;
            border: none;
            border-radius: 0;
            box-shadow: none;
            margin-top: 0;
        }
        /* Permanent Feedback Button */
        .feedback-float-btn {
            position: absolute;
            top: 30px;
            right: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 16px 28px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s;
        }
        .feedback-float-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
        }
        .feedback-title {
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 20px;
            color: #ffffff;
        }
        .feedback-buttons {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .feedback-btn {
            flex: 1;
            padding: 15px 30px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            color: #ffffff;
        }
        .feedback-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            background: rgba(255, 255, 255, 0.1);
        }
        .feedback-btn.thumbs-up {
            border-color: rgba(76, 175, 80, 0.5);
        }
        .feedback-btn.thumbs-up:hover,
        .feedback-btn.thumbs-up.active {
            background: rgba(76, 175, 80, 0.2);
            border-color: #4caf50;
            color: #4caf50;
            box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
        }
        .feedback-btn.thumbs-down {
            border-color: rgba(244, 67, 54, 0.5);
        }
        .feedback-btn.thumbs-down:hover,
        .feedback-btn.thumbs-down.active {
            background: rgba(244, 67, 54, 0.2);
            border-color: #f44336;
            color: #f44336;
            box-shadow: 0 8px 20px rgba(244, 67, 54, 0.3);
        }
        .feedback-comment {
            margin-top: 20px;
        }
        .feedback-comment textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            min-height: 100px;
            box-sizing: border-box;
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            transition: all 0.3s;
        }
        .feedback-comment textarea::placeholder {
            color: #8a8a9e;
        }
        .feedback-comment textarea:focus {
            outline: none;
            border-color: #667eea;
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        }
        .feedback-submit {
            margin-top: 15px;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        .feedback-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
        }
        .feedback-submit:disabled {
            background: rgba(255, 255, 255, 0.1);
            color: #8a8a9e;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .feedback-message {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            display: none;
        }
        .feedback-message.success {
            background: rgba(76, 175, 80, 0.2);
            color: #4caf50;
            border: 1px solid rgba(76, 175, 80, 0.4);
        }
        .feedback-message.error {
            background: rgba(244, 67, 54, 0.2);
            color: #f44336;
            border: 1px solid rgba(244, 67, 54, 0.4);
        }
        @media (max-width: 768px) {
            .categories-grid {
                grid-template-columns: 1fr;
            }
            .controls {
                flex-direction: column;
            }
            .form-group {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Feedback Button -->
        <button class="feedback-float-btn" onclick="openFeedbackModal()">
            💬 Feedback
        </button>
        
        <div class="header">
            <div class="hero-left">
                <span class="hero-badge">• AI-POWERED INTELLIGENCE</span>
                <h1>Anya</h1>
                <div class="header-subtitle">Your AI News Agent — Always On</div>
                
                <div class="header-tagline">
                    The latest breakthroughs across <span class="highlight">AI infrastructure</span>, <span class="highlight">applications</span>, <span class="highlight">tools</span> and <span class="highlight">startups</span>.
                </div>
                
                <div class="header-tagline">
                    Curated, synthesized, and delivered before your morning coffee.
                </div>
                
                <div class="header-tagline">
                    <strong style="color: #ffffff;">No noise. Just signal.</strong>
                </div>
            </div>
            
            <div class="hero-right">
                <div class="hero-character-container">
                    <svg class="anya-character" width="320" height="440" viewBox="0 0 320 440" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="bgGrad" x1="0" y1="0" x2="320" y2="440" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#1a1f3a"/>
              <stop offset="100%" stop-color="#0d1225"/>
            </linearGradient>
            <linearGradient id="skinGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#FDDBB4"/>
              <stop offset="100%" stop-color="#F5C49A"/>
            </linearGradient>
            <linearGradient id="hairGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#2D1B6E"/>
              <stop offset="100%" stop-color="#1a0f45"/>
            </linearGradient>
            <linearGradient id="shirtGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#1e2d5e"/>
              <stop offset="100%" stop-color="#0f1a3a"/>
            </linearGradient>
            <linearGradient id="laptopGrad" x1="0" y1="0" x2="320" y2="440" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#2a2a3e"/>
              <stop offset="100%" stop-color="#1a1a2e"/>
            </linearGradient>
            <linearGradient id="screenGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#0a0f2e"/>
              <stop offset="100%" stop-color="#060914"/>
            </linearGradient>
            <linearGradient id="glassesGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#7c6aff"/>
              <stop offset="100%" stop-color="#00f5c4"/>
            </linearGradient>
            <filter id="softGlow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
            <filter id="screenGlowFilter">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
            <clipPath id="screenClip">
              <rect x="88" y="268" width="144" height="90" rx="4"/>
            </clipPath>
          </defs>

          <!-- Background card -->
          <rect x="20" y="20" width="280" height="400" rx="24" fill="url(#bgGrad)" opacity="0.9"/>
          <rect x="20" y="20" width="280" height="400" rx="24" stroke="rgba(124,106,255,0.3)" stroke-width="1"/>

          <!-- ── BODY / CHAIR ── -->
          <rect x="110" y="330" width="100" height="80" rx="10" fill="#1a1f3a" stroke="rgba(124,106,255,0.2)" stroke-width="1"/>
          <ellipse cx="160" cy="380" rx="60" ry="12" fill="rgba(0,0,0,0.3)"/>

          <!-- ── TORSO / SHIRT ── -->
          <path d="M105 280 Q90 310 85 370 L235 370 Q230 310 215 280 Q190 295 160 295 Q130 295 105 280Z" fill="url(#shirtGrad)"/>
          <line x1="148" y1="295" x2="145" y2="330" stroke="#7c6aff" stroke-width="2" stroke-linecap="round"/>
          <line x1="172" y1="295" x2="175" y2="330" stroke="#7c6aff" stroke-width="2" stroke-linecap="round"/>
          <text x="145" y="325" font-family="monospace" font-size="11" fill="rgba(0,245,196,0.6)" text-anchor="middle">{ AI }</text>

          <!-- ── ARMS ── -->
          <path d="M105 285 Q75 310 78 345 Q82 355 90 350 Q95 330 110 310Z" fill="url(#skinGrad)"/>
          <path d="M215 285 Q245 310 242 345 Q238 355 230 350 Q225 330 210 310Z" fill="url(#skinGrad)"/>
          <ellipse cx="84" cy="348" rx="9" ry="6" fill="#FDDBB4" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>
          <ellipse cx="236" cy="348" rx="9" ry="6" fill="#FDDBB4" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/>

          <!-- Hands on laptop -->
          <ellipse cx="110" cy="360" rx="18" ry="10" fill="url(#skinGrad)" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/>
          <path d="M96 356 Q94 350 97 348 Q100 347 101 353" fill="url(#skinGrad)" stroke="rgba(200,150,100,0.3)" stroke-width="0.5"/>
          <path d="M103 354 Q101 347 104 345 Q107 344 108 351" fill="url(#skinGrad)" stroke="rgba(200,150,100,0.3)" stroke-width="0.5"/>
          <path d="M111 354 Q110 346 113 344 Q116 343 117 350" fill="url(#skinGrad)" stroke="rgba(200,150,100,0.3)" stroke-width="0.5"/>
          <path d="M119 355 Q119 348 122 347 Q125 347 125 353" fill="url(#skinGrad)" stroke="rgba(200,150,100,0.3)" stroke-width="0.5"/>
          <ellipse cx="210" cy="360" rx="18" ry="10" fill="url(#skinGrad)" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/>
          <path d="M196 356 Q194 349 197 347 Q200 346 201 353" fill="url(#skinGrad)" stroke="rgba(200,150,100,0.3)" stroke-width="0.5"/>
          <path d="M204 354 Q202 347 205 345 Q208 344 209 351" fill="url(#skinGrad)" stroke="rgba(200,150,100,0.3)" stroke-width="0.5"/>
          <path d="M212 354 Q211 346 214 344 Q217 343 218 350" fill="url(#skinGrad)" stroke="rgba(200,150,100,0.3)" stroke-width="0.5"/>
          <path d="M220 355 Q220 348 223 347 Q226 347 226 353" fill="url(#skinGrad)" stroke="rgba(200,150,100,0.3)" stroke-width="0.5"/>

          <!-- ── LAPTOP ── -->
          <rect x="75" y="355" width="170" height="22" rx="6" fill="url(#laptopGrad)" stroke="rgba(124,106,255,0.4)" stroke-width="1"/>
          <rect x="84" y="360" width="152" height="3" rx="1.5" fill="rgba(124,106,255,0.12)"/>
          <rect x="84" y="365" width="152" height="3" rx="1.5" fill="rgba(124,106,255,0.10)"/>
          <rect x="84" y="370" width="152" height="3" rx="1.5" fill="rgba(124,106,255,0.08)"/>
          <rect x="140" y="373" width="40" height="6" rx="2" fill="rgba(124,106,255,0.15)"/>

          <rect x="82" y="260" width="156" height="100" rx="8" fill="url(#laptopGrad)" stroke="rgba(124,106,255,0.5)" stroke-width="1.5"/>
          <rect x="88" y="268" width="144" height="90" rx="4" fill="url(#screenGrad)" class="screen-glow"/>

          <!-- Screen content -->
          <g clip-path="url(#screenClip)" class="screen-glow">
            <text x="93" y="281" font-family="monospace" font-size="6" fill="rgba(124,106,255,0.5)">01</text>
            <text x="93" y="290" font-family="monospace" font-size="6" fill="rgba(124,106,255,0.5)">02</text>
            <text x="93" y="299" font-family="monospace" font-size="6" fill="rgba(124,106,255,0.5)">03</text>
            <text x="93" y="308" font-family="monospace" font-size="6" fill="rgba(124,106,255,0.5)">04</text>
            <text x="93" y="317" font-family="monospace" font-size="6" fill="rgba(124,106,255,0.5)">05</text>
            <text x="93" y="326" font-family="monospace" font-size="6" fill="rgba(124,106,255,0.5)">06</text>
            <text x="93" y="335" font-family="monospace" font-size="6" fill="rgba(124,106,255,0.5)">07</text>
            <text x="93" y="344" font-family="monospace" font-size="6" fill="rgba(124,106,255,0.5)">08</text>
            <text x="108" y="281" font-family="monospace" font-size="6.5" fill="#7c6aff">import</text>
            <text x="133" y="281" font-family="monospace" font-size="6.5" fill="#e8eaf6"> anya</text>
            <text x="108" y="290" font-family="monospace" font-size="6.5" fill="#00f5c4">fetch</text>
            <text x="127" y="290" font-family="monospace" font-size="6.5" fill="#e8eaf6">(news.ai)</text>
            <text x="108" y="299" font-family="monospace" font-size="6.5" fill="#ff6b9d">filter</text>
            <text x="128" y="299" font-family="monospace" font-size="6.5" fill="#e8eaf6">(signal)</text>
            <text x="108" y="308" font-family="monospace" font-size="6.5" fill="#00f5c4">rank</text>
            <text x="122" y="308" font-family="monospace" font-size="6.5" fill="#e8eaf6">(impact)</text>
            <text x="108" y="317" font-family="monospace" font-size="6.5" fill="#7c6aff">deliver</text>
            <text x="131" y="317" font-family="monospace" font-size="6.5" fill="#e8eaf6">(you)</text>
            <text x="108" y="326" font-family="monospace" font-size="6.5" fill="#e8eaf6">// ✓ 85 sources</text>
            <text x="108" y="335" font-family="monospace" font-size="6.5" fill="rgba(255,255,255,0.3)">// ✓ realtime</text>
            <rect x="108" y="340" width="5" height="8" rx="1" fill="#00f5c4" class="cursor-blink">
              <animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>
            </rect>
          </g>

          <path d="M90 270 L170 270 L155 280 L90 280Z" fill="rgba(255,255,255,0.03)"/>
          <circle cx="160" cy="256" r="5" fill="none" stroke="rgba(124,106,255,0.3)" stroke-width="1"/>

          <!-- ── NECK ── -->
          <rect x="150" y="220" width="20" height="30" rx="8" fill="url(#skinGrad)"/>

          <!-- ── HEAD ── -->
          <ellipse cx="160" cy="195" rx="52" ry="58" fill="url(#skinGrad)"/>

          <!-- ── HAIR ── -->
          <ellipse cx="160" cy="170" rx="56" ry="62" fill="url(#hairGrad)"/>
          <path d="M108 185 Q95 200 100 230 Q108 250 118 245 Q110 220 112 195Z" fill="url(#hairGrad)"/>
          <path d="M212 185 Q225 200 220 230 Q212 250 202 245 Q210 220 208 195Z" fill="url(#hairGrad)"/>
          <path d="M108 155 Q120 120 160 115 Q200 120 212 155 Q195 135 160 132 Q125 135 108 155Z" fill="#3d2fa0"/>
          <path d="M130 125 Q140 118 150 120" stroke="#7c6aff" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
          <path d="M155 117 Q165 113 175 116" stroke="#7c6aff" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
          <path d="M108 155 Q115 140 125 135" stroke="rgba(61,47,160,0.8)" stroke-width="2" stroke-linecap="round" fill="none"/>
          <path d="M212 155 Q205 140 195 135" stroke="rgba(61,47,160,0.8)" stroke-width="2" stroke-linecap="round" fill="none"/>
          <path d="M108 185 Q106 200 108 215 Q114 205 116 195Z" fill="#2D1B6E"/>
          <path d="M212 185 Q214 200 212 215 Q206 205 204 195Z" fill="#2D1B6E"/>

          <!-- ── EARS ── -->
          <ellipse cx="109" cy="200" rx="7" ry="9" fill="url(#skinGrad)"/>
          <ellipse cx="211" cy="200" rx="7" ry="9" fill="url(#skinGrad)"/>
          <path d="M110 195 Q108 200 110 205" stroke="rgba(200,150,100,0.4)" stroke-width="1" fill="none"/>
          <path d="M210 195 Q212 200 210 205" stroke="rgba(200,150,100,0.4)" stroke-width="1" fill="none"/>
          <circle cx="109" cy="208" r="3" fill="#7c6aff" filter="url(#softGlow)"/>
          <circle cx="211" cy="208" r="3" fill="#7c6aff" filter="url(#softGlow)"/>

          <!-- ── FACE ── -->
          <ellipse cx="160" cy="200" rx="48" ry="52" fill="url(#skinGrad)"/>

          <!-- ── GLASSES ── -->
          <line x1="145" y1="193" x2="175" y2="193" stroke="url(#glassesGrad)" stroke-width="2"/>
          <rect x="118" y="183" width="27" height="20" rx="8" fill="rgba(124,106,255,0.1)" stroke="url(#glassesGrad)" stroke-width="2" filter="url(#softGlow)"/>
          <rect x="175" y="183" width="27" height="20" rx="8" fill="rgba(124,106,255,0.1)" stroke="url(#glassesGrad)" stroke-width="2" filter="url(#softGlow)"/>
          <path d="M121 186 Q126 184 130 186" stroke="rgba(255,255,255,0.4)" stroke-width="1" stroke-linecap="round"/>
          <path d="M178 186 Q183 184 187 186" stroke="rgba(255,255,255,0.4)" stroke-width="1" stroke-linecap="round"/>
          <path d="M118 190 Q108 190 107 188" stroke="url(#glassesGrad)" stroke-width="2" stroke-linecap="round" fill="none"/>
          <path d="M202 190 Q212 190 213 188" stroke="url(#glassesGrad)" stroke-width="2" stroke-linecap="round" fill="none"/>

          <!-- ── EYES ── -->
          <ellipse cx="131" cy="193" rx="7" ry="7" fill="#1a0f3a"/>
          <ellipse cx="131" cy="193" rx="5" ry="5" fill="#4a2fa0"/>
          <ellipse cx="131" cy="193" rx="3" ry="3" fill="#1a0a2e"/>
          <circle cx="131" cy="193" r="3" fill="#2d1b6e"/>
          <circle cx="131" cy="193" r="1.5" fill="#060914"/>
          <circle cx="133" cy="191" r="1.2" fill="white" opacity="0.9"/>
          <circle cx="129" cy="194" r="0.7" fill="white" opacity="0.5"/>

          <ellipse cx="189" cy="193" rx="7" ry="7" fill="#1a0f3a"/>
          <ellipse cx="189" cy="193" rx="5" ry="5" fill="#4a2fa0"/>
          <ellipse cx="189" cy="193" rx="3" ry="3" fill="#1a0a2e"/>
          <circle cx="189" cy="193" r="3" fill="#2d1b6e"/>
          <circle cx="189" cy="193" r="1.5" fill="#060914"/>
          <circle cx="191" cy="191" r="1.2" fill="white" opacity="0.9"/>
          <circle cx="187" cy="194" r="0.7" fill="white" opacity="0.5"/>

          <!-- Eyelashes -->
          <path d="M124 189 Q122 185 121 184" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M127 187 Q126 183 126 182" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M131 186 Q131 182 132 181" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M135 187 Q136 183 137 183" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M138 189 Q140 186 141 186" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>

          <path d="M182 189 Q180 185 179 184" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M185 187 Q184 183 184 182" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M189 186 Q189 182 190 181" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M193 187 Q194 183 195 183" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M196 189 Q198 186 199 186" stroke="#1a0f3a" stroke-width="1.5" stroke-linecap="round"/>

          <path d="M121 182 Q131 177 141 180" stroke="#2D1B6E" stroke-width="3" stroke-linecap="round" fill="none"/>
          <path d="M179 180 Q189 177 199 182" stroke="#2D1B6E" stroke-width="3" stroke-linecap="round" fill="none"/>

          <!-- ── NOSE ── -->
          <path d="M157 200 Q155 212 152 215 Q157 218 163 215 Q168 212 163 200Z" fill="rgba(200,140,90,0.3)" stroke="none"/>
          <path d="M153 215 Q157 218 163 215" stroke="rgba(180,120,80,0.5)" stroke-width="1.2" fill="none" stroke-linecap="round"/>

          <!-- ── MOUTH ── -->
          <path d="M147 228 Q160 240 173 228" stroke="#c67b5e" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <path d="M148 228 Q160 235 172 228 Q160 233 148 228Z" fill="rgba(198,123,94,0.3)"/>
          <path d="M152 229 Q160 235 168 229" stroke="rgba(255,255,255,0.2)" stroke-width="1" fill="none"/>

          <ellipse cx="122" cy="218" rx="12" ry="7" fill="rgba(255,107,157,0.12)"/>
          <ellipse cx="198" cy="218" rx="12" ry="7" fill="rgba(255,107,157,0.12)"/>

          <!-- ── HEADPHONES ── -->
          <path d="M112 175 Q110 140 160 132 Q210 140 208 175" stroke="#2a2a4e" stroke-width="6" fill="none" stroke-linecap="round"/>
          <path d="M112 175 Q110 140 160 132 Q210 140 208 175" stroke="rgba(124,106,255,0.4)" stroke-width="2" fill="none" stroke-linecap="round"/>
          <rect x="104" y="172" width="16" height="22" rx="7" fill="#1a1f3a" stroke="rgba(124,106,255,0.5)" stroke-width="1.5"/>
          <rect x="107" y="176" width="10" height="14" rx="4" fill="#7c6aff" opacity="0.3"/>
          <rect x="200" y="172" width="16" height="22" rx="7" fill="#1a1f3a" stroke="rgba(124,106,255,0.5)" stroke-width="1.5"/>
          <rect x="203" y="176" width="10" height="14" rx="4" fill="#7c6aff" opacity="0.3"/>
          <circle cx="112" cy="178" r="2.5" fill="#00f5c4" filter="url(#softGlow)" opacity="0.9"/>
          <circle cx="208" cy="178" r="2.5" fill="#00f5c4" filter="url(#softGlow)" opacity="0.9"/>

          <ellipse cx="160" cy="210" rx="40" ry="35" fill="rgba(0,245,196,0.04)" class="screen-glow"/>

          <!-- ── NAME TAG ── -->
          <rect x="105" y="385" width="110" height="24" rx="6" fill="rgba(124,106,255,0.15)" stroke="rgba(124,106,255,0.3)" stroke-width="1"/>
          <text x="160" y="402" font-family="monospace" font-size="10" fill="#00f5c4" text-anchor="middle" font-weight="700">ANYA.AI</text>
          <circle cx="115" cy="397" r="3" fill="#00f5c4"/>

        </svg>
                </div>
            </div>
        </div>

        <div class="controls">
            <div class="form-group days-group">
                <label for="days">Days to look back</label>
                <input type="number" id="days" name="days" value="7" min="1" max="30">
            </div>
            <div class="form-group mode-group">
                <label for="mode">Mode</label>
                <select id="mode" name="mode">
                    <option value="fast">Fast Mode (RSS summaries)</option>
                    <option value="full">Full Mode (AI summaries)</option>
                </select>
            </div>
            <div class="form-group">
                <button type="button" class="btn" id="submitBtn" onclick="window.runAgent && window.runAgent()">Fetch Latest News</button>
            </div>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="font-size: 1.1em; margin-top: 20px;">Curating 85 sources to get you the most relevant and current AI news. This may take a minute or two. Please wait...</p>
        </div>

        <div id="errorContainer"></div>

        <!-- Modal for Full Summary -->
        <div id="summaryModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title" id="modalTitle">Category Summary</div>
                    <span class="close-modal" onclick="closeSummaryModal()">&times;</span>
                </div>
                <div class="modal-body" id="modalBody"></div>
            </div>
        </div>

        <div class="results" id="results">
            <div class="categories-grid" id="categoriesGrid"></div>
            
            <!-- Email Section (appears after results) -->
            <div class="email-section" id="emailSection" style="display: none;">
                <div class="email-title">📧 Send Summary via Email</div>
                <div class="email-form">
                    <input type="email" id="emailInput" placeholder="Enter your email address" class="email-input">
                    <button class="email-send-btn" id="emailSendBtn" onclick="sendEmail()">Send Email</button>
                </div>
                <div class="email-message" id="emailMessage"></div>
            </div>
        </div>
    </div>
    
    <!-- Feedback Modal -->
    <div class="modal-overlay" id="feedbackModal">
        <div class="modal-content">
            <button class="modal-close" onclick="closeFeedbackModal()">×</button>
            <div class="feedback-section">
                <div class="feedback-title">💬 How was your experience?</div>
                <div class="feedback-buttons">
                    <button class="feedback-btn thumbs-up" onclick="selectFeedback('thumbs_up')">
                        👍 Thumbs Up
                    </button>
                    <button class="feedback-btn thumbs-down" onclick="selectFeedback('thumbs_down')">
                        👎 Thumbs Down
                    </button>
                </div>
                <div class="feedback-comment">
                    <textarea id="feedbackComment" placeholder="Optional: Tell us more about your experience..."></textarea>
                </div>
                <button class="feedback-submit" id="feedbackSubmit" onclick="submitFeedback()" disabled>
                    Submit Feedback
                </button>
                <div class="feedback-message" id="feedbackMessage"></div>
            </div>
        </div>
    </div>

    <script>
        const categoryConfig = {
            "GPU and AI Infra": { icon: "⚙️", color: "#667eea" },
            "AI Applications": { icon: "✨", color: "#4facfe" },
            "AI Builder tools": { icon: "🔨", color: "#f093fb" },
            "AI startups to watch": { icon: "🚀", color: "#fa709a" }
        };

        // Modal Functions
        function openEmailModal() {
            document.getElementById('emailModal').classList.add('active');
        }
        
        function closeEmailModal() {
            document.getElementById('emailModal').classList.remove('active');
        }
        
        function openFeedbackModal() {
            document.getElementById('feedbackModal').classList.add('active');
        }
        
        function closeFeedbackModal() {
            document.getElementById('feedbackModal').classList.remove('active');
        }
        
        // Close modals when clicking outside
        document.addEventListener('click', function(event) {
            const emailModal = document.getElementById('emailModal');
            const feedbackModal = document.getElementById('feedbackModal');
            
            if (event.target === emailModal) {
                closeEmailModal();
            }
            if (event.target === feedbackModal) {
                closeFeedbackModal();
            }
        });
        
        // Close modals with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeEmailModal();
                closeFeedbackModal();
            }
        });

        // Make runAgent globally accessible (both ways for compatibility)
        async function runAgent() {
            console.log('runAgent() called');
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const errorContainer = document.getElementById('errorContainer');
            const categoriesGrid = document.getElementById('categoriesGrid');
            
            if (!submitBtn || !loading || !results || !errorContainer || !categoriesGrid) {
                console.error('Missing required elements:', {submitBtn, loading, results, errorContainer, categoriesGrid});
                alert('Error: Page elements not loaded. Please refresh the page.');
                return;
            }
            
            console.log('Starting agent...');
            // Reset UI
            submitBtn.disabled = true;
            submitBtn.textContent = 'Curating...';
            loading.style.display = 'block';
            results.classList.remove('visible');
            errorContainer.innerHTML = '';
            categoriesGrid.innerHTML = '';
            
            const formData = {
                days: parseInt(document.getElementById('days').value),
                mode: document.getElementById('mode').value,
                fetchContent: false
            };
            
            // Update loading message
            const loadingText = loading.querySelector('p');
            const originalText = loadingText.textContent;
            loadingText.textContent = 'Curating 85 sources to get you the most relevant and current AI news. This may take a minute or two. Please wait...';
            
            try {
                const response = await fetch('/run', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('Server error response:', errorText);
                    throw new Error(`Server error: ${response.status} ${response.statusText}`);
                }
                
                const data = await response.json();
                console.log('Response received:', data);
                console.log('Categories:', Object.keys(data.categories || {}));
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Verify we have data
                const totalArticles = Object.values(data.categories || {}).reduce((sum, cat) => {
                    const articles = Array.isArray(cat) ? cat : (cat.articles || []);
                    return sum + articles.length;
                }, 0);
                console.log(`Total articles in response: ${totalArticles}`);
                
                if (totalArticles === 0) {
                    errorContainer.innerHTML = `<div class="error"><strong>No articles found</strong><br><small>Try increasing "Days to look back" or check if news sources are available.</small></div>`;
                    return;
                }
                
                displayResults(data);
                
            } catch (error) {
                console.error('Error:', error);
                console.error('Error stack:', error.stack);
                errorContainer.innerHTML = `<div class="error"><strong>Error:</strong> ${error.message}<br><small>Check the browser console (F12) for more details.</small></div>`;
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Fetch Latest News';
                loading.style.display = 'none';
                if (loadingText) {
                    loadingText.textContent = originalText;
                }
            }
        }
        
        // Also assign to window for explicit access
        window.runAgent = runAgent;
        
        function displayResults(data) {
            console.log('displayResults called with:', data);
            const results = document.getElementById('results');
            const categoriesGrid = document.getElementById('categoriesGrid');
            
            // Clear previous results
            categoriesGrid.innerHTML = '';
            
            // Create category boxes
            const categoryOrder = [
                "GPU and AI Infra",
                "AI Applications", 
                "AI Builder tools",
                "AI startups to watch"
            ];
            
            categoryOrder.forEach(categoryName => {
                const config = categoryConfig[categoryName] || { icon: "📰", color: "#667eea" };
                const categoryData = data.categories && data.categories[categoryName];
                
                console.log(`Processing ${categoryName}:`, categoryData);
                
                // Handle response format: {summary: ..., articles: [...]}
                let articles = [];
                let categorySummary = null;
                
                if (categoryData) {
                    if (Array.isArray(categoryData)) {
                        // Old format: just an array
                        articles = categoryData;
                        console.log(`  Found ${articles.length} articles (array format)`);
                    } else if (categoryData.articles) {
                        // New format: {summary: ..., articles: [...]}
                        articles = categoryData.articles || [];
                        categorySummary = categoryData.summary || null;
                        console.log(`  Found ${articles.length} articles, summary: ${categorySummary ? 'Yes' : 'No'}`);
                    } else {
                        console.log(`  Category data exists but no articles field`);
                    }
                } else {
                    console.log(`  No data for ${categoryName}`);
                }
                
                const categoryBox = document.createElement('div');
                categoryBox.className = 'category-box';
                categoryBox.style.borderColor = config.color;
                categoryBox.setAttribute('data-category', categoryName);
                
                const header = document.createElement('div');
                header.className = 'category-header';
                header.style.color = config.color;
                header.innerHTML = `
                    <div class="category-icon">${config.icon}</div>
                    <div class="category-title">${categoryName}</div>
                    <div class="category-count">${articles.length} article${articles.length !== 1 ? 's' : ''}</div>
                `;
                
                const content = document.createElement('div');
                content.className = 'category-content';
                
                if (articles.length === 0) {
                    content.innerHTML = '<div class="empty-state">No articles found in this category</div>';
                } else {
                    // Category Overview Section - Only show in Full Mode or if summary exists
                    const isFullMode = data.mode === 'full';
                    if (isFullMode || categorySummary) {
                        const overviewDiv = document.createElement('div');
                        overviewDiv.className = 'category-overview';
                        overviewDiv.style.borderLeftColor = config.color;
                        if (categorySummary) {
                            // Truncate summary to first 2-3 sentences (approximately 200 characters)
                            const sentences = categorySummary.match(/[^.!?]+[.!?]+/g) || [categorySummary];
                            const previewSentences = sentences.slice(0, 2).join(' ');
                            const previewText = previewSentences.length < categorySummary.length 
                                ? previewSentences 
                                : categorySummary.substring(0, 200) + '...';
                            const showReadMore = categorySummary.length > previewText.length;
                            
                            // Store full summary in data attribute
                            overviewDiv.setAttribute('data-full-summary', categorySummary);
                            overviewDiv.setAttribute('data-category-name', categoryName);
                            
                            overviewDiv.innerHTML = `
                                <div class="category-overview-title">
                                    <span>📊</span>
                                    <span>AI-Generated Category Summary</span>
                                </div>
                                <div class="category-overview-text">
                                    ${escapeHtml(previewText)}
                                    ${showReadMore ? `<span class="read-more-link" onclick="showFullSummaryFromElement(this)">Read more</span>` : ''}
                                </div>
                            `;
                        } else {
                            // Only show API key error in Full Mode when summary is missing
                            overviewDiv.innerHTML = `
                                <div class="category-overview-title">
                                    <span>📊</span>
                                    <span>Category Overview</span>
                                </div>
                                <div class="category-overview-text" style="color: #d32f2f; font-weight: 500; padding: 15px; background: #ffebee; border-radius: 8px; border-left: 3px solid #d32f2f;">
                                    <strong>⚠️ API Key Required</strong><br><br>
                                    Category summaries require a valid OpenAI API key.<br><br>
                                    <strong>To fix this:</strong><br>
                                    1. Open <code>~/ai_news_agent/.env</code> in a text editor<br>
                                    2. Replace <code>your_openai_api_key_here</code> with your actual OpenAI API key<br>
                                    3. Your key should start with <code>sk-</code><br>
                                    4. Restart the server and try Full Mode again<br><br>
                                    <small>Get your API key at: <a href="https://platform.openai.com/account/api-keys" target="_blank">platform.openai.com/account/api-keys</a></small>
                                </div>
                            `;
                        }
                        // Add overview FIRST
                        content.appendChild(overviewDiv);
                    }
                    
                    // Articles Section (expandable) - Show AFTER overview
                    const articlesSection = document.createElement('div');
                    articlesSection.className = 'articles-section';
                    
                    const articlesToggle = document.createElement('div');
                    articlesToggle.className = 'articles-toggle';
                    articlesToggle.style.color = config.color;
                    articlesToggle.innerHTML = `
                        <div class="articles-toggle-title">📰 View Individual Articles (${articles.length})</div>
                        <div class="articles-toggle-icon">▼</div>
                    `;
                    // Start collapsed by default
                    articlesToggle.classList.remove('expanded');
                    
                    const articlesContainer = document.createElement('div');
                    articlesContainer.className = 'articles-container';
                    
                    const articlesList = document.createElement('div');
                    articlesList.className = 'articles-list';
                    
                    articles.forEach(article => {
                        const summary = article.ai_summary || article.summary || 'No summary available';
                        const summaryText = summary.length > 200 ? summary.substring(0, 200) + '...' : summary;
                        const daysAgo = article.days_ago !== null ? `${article.days_ago} days ago` : '';
                        const focus = article.focus || '';
                        
                        const articleCard = document.createElement('div');
                        articleCard.className = 'article-card';
                        articleCard.style.borderLeftColor = config.color;
                        articleCard.innerHTML = `
                            <div class="article-title">
                                <a href="${article.link}" target="_blank">${escapeHtml(article.title)}</a>
                            </div>
                            <div class="article-meta">
                                <span><strong>Source:</strong> ${escapeHtml(article.source)}</span>
                                ${daysAgo ? `<span><strong>Published:</strong> ${daysAgo}</span>` : ''}
                                ${focus ? `<span><strong>Focus:</strong> ${escapeHtml(focus)}</span>` : ''}
                            </div>
                            <div class="article-summary">${escapeHtml(summaryText)}</div>
                            <a href="${article.link}" target="_blank" class="read-more">Visit Website</a>
                        `;
                        articlesList.appendChild(articleCard);
                    });
                    
                    articlesContainer.appendChild(articlesList);
                    
                    // Toggle articles section
                    articlesToggle.addEventListener('click', () => {
                        articlesToggle.classList.toggle('expanded');
                    });
                    
                    articlesSection.appendChild(articlesToggle);
                    articlesSection.appendChild(articlesContainer);
                    // Always append articles section to content
                    content.appendChild(articlesSection);
                    
                    // Debug: Log that articles section was added
                    console.log(`✅ Articles section added for ${categoryName} with ${articles.length} articles`);
                }
                
                // Toggle expand/collapse category
                header.addEventListener('click', () => {
                    categoryBox.classList.toggle('expanded');
                });
                
                categoryBox.appendChild(header);
                categoryBox.appendChild(content);
                categoriesGrid.appendChild(categoryBox);
            });
            
            results.classList.add('visible');
            
            // Show email section after results are displayed
            const emailSection = document.getElementById('emailSection');
            if (emailSection) {
                emailSection.style.display = 'block';
            }
        }
        
        let selectedFeedback = null;
        
        function selectFeedback(type) {
            selectedFeedback = type;
            
            // Update button states
            document.querySelectorAll('.feedback-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            const btn = type === 'thumbs_up' 
                ? document.querySelector('.thumbs-up')
                : document.querySelector('.thumbs-down');
            if (btn) {
                btn.classList.add('active');
            }
            
            // Enable submit button
            const submitBtn = document.getElementById('feedbackSubmit');
            if (submitBtn) {
                submitBtn.disabled = false;
            }
        }
        
        async function submitFeedback() {
            if (!selectedFeedback) {
                return;
            }
            
            const comment = document.getElementById('feedbackComment').value.trim();
            const submitBtn = document.getElementById('feedbackSubmit');
            const messageDiv = document.getElementById('feedbackMessage');
            
            // Disable submit button
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            try {
                const response = await fetch('/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        feedback: selectedFeedback,
                        comment: comment
                    })
                });
                
                if (response.ok) {
                    // Show success message
                    messageDiv.className = 'feedback-message success';
                    messageDiv.textContent = '✅ Thank you for your feedback!';
                    messageDiv.style.display = 'block';
                    
                    // Reset form after 3 seconds
                    setTimeout(() => {
                        selectedFeedback = null;
                        document.getElementById('feedbackComment').value = '';
                        document.querySelectorAll('.feedback-btn').forEach(btn => {
                            btn.classList.remove('active');
                        });
                        submitBtn.disabled = true;
                        submitBtn.textContent = 'Submit Feedback';
                        messageDiv.style.display = 'none';
                    }, 3000);
                } else {
                    throw new Error('Failed to submit feedback');
                }
            } catch (error) {
                messageDiv.className = 'feedback-message error';
                messageDiv.textContent = '❌ Error submitting feedback. Please try again.';
                messageDiv.style.display = 'block';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Feedback';
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        window.showFullSummaryFromElement = function(element) {
            const overviewDiv = element.closest('.category-overview');
            const categoryName = overviewDiv.getAttribute('data-category-name');
            const fullSummary = overviewDiv.getAttribute('data-full-summary');
            showFullSummary(categoryName, fullSummary);
        }
        
        window.showFullSummary = function(categoryName, fullSummary) {
            const modal = document.getElementById('summaryModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modalTitle.textContent = `${categoryName} - Full Summary`;
            const summaryWithBreaks = escapeHtml(fullSummary).split('\\n').join('<br>');
            modalBody.innerHTML = summaryWithBreaks;
            modal.style.display = 'block';
        }
        
        window.closeSummaryModal = function() {
            const modal = document.getElementById('summaryModal');
            modal.style.display = 'none';
        }
        
        // Close modal when clicking outside of it
        window.onclick = function(event) {
            const modal = document.getElementById('summaryModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
        
        // Store current results data for email
        let currentResultsData = null;
        
        // Update displayResults to store data
        const originalDisplayResults = displayResults;
        displayResults = function(data) {
            currentResultsData = data;
            originalDisplayResults(data);
        };
        
        // Send email function
        window.sendEmail = async function() {
            const emailInput = document.getElementById('emailInput');
            const emailSendBtn = document.getElementById('emailSendBtn');
            const messageDiv = document.getElementById('emailMessage');
            
            const email = emailInput.value.trim();
            if (!email) {
                messageDiv.className = 'email-message error';
                messageDiv.textContent = '❌ Please enter an email address';
                messageDiv.style.display = 'block';
                return;
            }
            
            // Basic email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                messageDiv.className = 'email-message error';
                messageDiv.textContent = '❌ Please enter a valid email address';
                messageDiv.style.display = 'block';
                return;
            }
            
            if (!currentResultsData) {
                messageDiv.className = 'email-message error';
                messageDiv.textContent = '❌ No results to send. Please fetch news first.';
                messageDiv.style.display = 'block';
                return;
            }
            
            // Disable button
            emailSendBtn.disabled = true;
            emailSendBtn.textContent = 'Sending...';
            messageDiv.style.display = 'none';
            
            try {
                const response = await fetch('/send-email', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        results: currentResultsData
                    })
                });
                
                // Check if response is JSON
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    const text = await response.text();
                    console.error('Server returned non-JSON response:', text.substring(0, 200));
                    throw new Error('Server error. Please check Railway logs or email configuration.');
                }
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    messageDiv.className = 'email-message success';
                    messageDiv.textContent = '✅ Email sent successfully! Check your inbox.';
                    messageDiv.style.display = 'block';
                    emailInput.value = '';
                } else {
                    const errorMsg = data.error || data.details || 'Failed to send email';
                    throw new Error(errorMsg);
                }
            } catch (error) {
                console.error('Email send error:', error);
                messageDiv.className = 'email-message error';
                messageDiv.textContent = `❌ ${error.message}`;
                messageDiv.style.display = 'block';
            } finally {
                emailSendBtn.disabled = false;
                emailSendBtn.textContent = 'Send Email';
            }
        };
        
        // Ensure button is clickable on page load
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, setting up button...');
            const submitBtn = document.getElementById('submitBtn');
            if (submitBtn) {
                console.log('✅ Submit button found');
                // Remove any disabled attribute
                submitBtn.disabled = false;
                // Add event listener as backup to onclick
                submitBtn.addEventListener('click', function(e) {
                    console.log('Button clicked via event listener');
                    e.preventDefault();
                    if (window.runAgent) {
                        window.runAgent();
                    } else {
                        console.error('window.runAgent is not defined!');
                        alert('Error: runAgent function not found. Please refresh the page.');
                    }
                });
                console.log('✅ Event listener added to button');
            } else {
                console.error('❌ Submit button not found!');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/health')
def health():
    """Health check endpoint for Railway."""
    return jsonify({"status": "healthy", "service": "AI News Agent"}), 200

@app.route('/test')
def test():
    """Simple test endpoint."""
    return "AI News Agent is running!", 200

@app.route('/')
def index():
    """Render the main page."""
    try:
        return render_template_string(HTML_TEMPLATE)
    except Exception as e:
        print(f"Error rendering template: {e}")
        traceback.print_exc()
        return f"Error: {str(e)}", 500

@app.route('/run', methods=['POST'])
def run_agent():
    """Run the AI News Agent and return results."""
    try:
        data = request.json
        days = data.get('days', 7)
        mode = data.get('mode', 'fast')
        fetch_content = data.get('fetchContent', False)
        
        # Determine settings based on mode
        fetch_full_content = fetch_content if mode == 'full' else False
        generate_summaries = mode == 'full'
        
        # Initialize and run agent
        agent = AINewsAgent()
        results = agent.run(
            days=days,
            fetch_full_content=fetch_full_content,
            generate_summaries=generate_summaries
        )
        
        # Ensure all 4 categories are present
        all_categories = {
            "GPU and AI Infra": [],
            "AI Applications": [],
            "AI Builder tools": [],
            "AI startups to watch": []
        }
        
        # Prepare response
        response_data = {
            "generated_at": datetime.now().isoformat(),
            "mode": mode,  # Include mode so frontend knows if it's Fast or Full
            "categories": {}
        }
        
        for category in all_categories.keys():
            articles = results.get(category, [])
            response_data["categories"][category] = {
                "summary": None,  # Category-level summary
                "articles": []
            }
            
            # Get category summary from first article (if available)
            category_summary = None
            if articles:
                # Try to get category summary from any article
                for article in articles:
                    if article.get("category_summary"):
                        category_summary = article.get("category_summary")
                        break
            
            response_data["categories"][category]["summary"] = category_summary
            print(f"DEBUG: {category} - {len(articles)} articles, summary: {'Yes' if category_summary else 'No'}")
            
            for article in articles:
                    # Clean HTML from summaries
                    summary = article.get("summary", "") or article.get("description", "")
                    if summary:
                        # Remove HTML tags
                        import re
                        summary = re.sub('<[^<]+?>', '', summary)
                        summary = summary.strip()
                    
                    article_data = {
                        "title": article.get("title", "No title"),
                        "source": article.get("source", "Unknown"),
                        "link": article.get("link", "#"),
                        "published": article.get("published", ""),
                        "days_ago": article.get("days_ago"),
                        "summary": summary[:500] if summary else "",  # Limit summary length
                        "ai_summary": article.get("ai_summary"),
                        "focus": article.get("focus", "")  # For startups
                    }
                    response_data["categories"][category]["articles"].append(article_data)
        
        return jsonify(response_data)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in /run endpoint: {e}")
        print(error_trace)
        return jsonify({
            "error": str(e),
            "traceback": error_trace
        }), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Save user feedback to CSV file."""
    try:
        data = request.json
        feedback_type = data.get('feedback', '')
        comment = data.get('comment', '')
        
        if not feedback_type:
            return jsonify({"error": "Feedback type is required"}), 400
        
        # Get the directory where the app is running
        app_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(app_dir, 'feedback.csv')
        
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_file)
        
        # Write to CSV
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow(['timestamp', 'feedback', 'comment'])
            
            # Write feedback data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, feedback_type, comment])
        
        return jsonify({
            "success": True,
            "message": "Feedback saved successfully"
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error saving feedback: {e}")
        print(error_trace)
        return jsonify({
            "error": str(e),
            "traceback": error_trace
        }), 500

def generate_email_html(results_data, app_url="http://localhost:5001"):
    """Generate beautiful HTML email with news summary."""
    categories = results_data.get('categories', {})
    generated_at = results_data.get('generated_at', datetime.now().isoformat())
    
    # Format date
    try:
        date_obj = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
        formatted_date = date_obj.strftime('%B %d, %Y at %I:%M %p')
    except:
        formatted_date = generated_at
    
    # Build category sections
    category_html = ""
    category_config = {
        "GPU and AI Infra": {"icon": "⚙️", "color": "#667eea"},
        "AI Applications": {"icon": "✨", "color": "#4facfe"},
        "AI Builder tools": {"icon": "🔨", "color": "#f093fb"},
        "AI startups to watch": {"icon": "🚀", "color": "#fa709a"}
    }
    
    for category_name, cat_data in categories.items():
        if isinstance(cat_data, dict):
            articles = cat_data.get('articles', [])
            summary = cat_data.get('summary', '')
        else:
            articles = cat_data if isinstance(cat_data, list) else []
            summary = ''
        
        if not articles:
            continue
        
        config = category_config.get(category_name, {"icon": "📰", "color": "#667eea"})
        
        # Category summary (first 2 sentences)
        summary_preview = ""
        if summary:
            sentences = summary.split('. ')
            preview_sentences = sentences[:2]
            summary_preview = '. '.join(preview_sentences)
            if len(sentences) > 2:
                summary_preview += '...'
        
        category_html += f"""
        <tr>
            <td style="padding: 25px; background: linear-gradient(135deg, rgba({int(config['color'][1:3], 16)}, {int(config['color'][3:5], 16)}, {int(config['color'][5:7], 16)}, 0.08) 0%, rgba({int(config['color'][1:3], 16)}, {int(config['color'][3:5], 16)}, {int(config['color'][5:7], 16)}, 0.15) 100%); border-radius: 16px; border: 1px solid rgba({int(config['color'][1:3], 16)}, {int(config['color'][3:5], 16)}, {int(config['color'][5:7], 16)}, 0.3); margin-bottom: 20px;">
                <h2 style="margin: 0 0 12px 0; color: {config['color']}; font-size: 20px; font-weight: 700; font-family: 'Space Grotesk', sans-serif;">
                    {config['icon']} {category_name}
                </h2>
                {f'<p style="color: #b4b4c8; line-height: 1.7; margin-bottom: 18px; font-size: 14px;">{html.escape(summary_preview)}</p>' if summary_preview else ''}
                <p style="color: #8a8a9e; margin: 10px 0; font-weight: 600; font-size: 13px;">● {len(articles)} Article{'' if len(articles) == 1 else 's'}</p>
                <ul style="list-style: none; padding: 0; margin: 15px 0 0 0;">
        """
        
        for article in articles[:5]:  # Show top 5 articles
            title = article.get('title', 'No title')
            link = article.get('link', '#')
            source = article.get('source', 'Unknown')
            category_html += f"""
                    <li style="margin-bottom: 12px; padding: 16px; background: rgba(255, 255, 255, 0.03); border-radius: 10px; border-left: 3px solid {config['color']}; backdrop-filter: blur(10px);">
                        <a href="{link}" style="color: #e0e0e8; text-decoration: none; font-weight: 600; font-size: 15px; display: block; margin-bottom: 6px; line-height: 1.4;">
                            {html.escape(title)}
                        </a>
                        <span style="color: #8a8a9e; font-size: 13px;">📰 {html.escape(source)}</span>
                    </li>
            """
        
        if len(articles) > 5:
            category_html += f"""
                    <li style="text-align: center; margin-top: 15px; padding: 10px;">
                        <span style="color: #6b7280; font-size: 13px;">... and {len(articles) - 5} more articles in full report</span>
                    </li>
            """
        
        category_html += """
                </ul>
            </td>
        </tr>
        """
    
    email_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
        <title>Your AI News Summary from Anya</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background-color: #0a0a0f;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #0a0a0f; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #0d1225; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.5); border: 1px solid rgba(139, 132, 255, 0.2);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 100%); padding: 50px 30px; text-align: center; position: relative;">
                                <div style="display: inline-block; padding: 6px 14px; background: rgba(139, 132, 255, 0.2); border: 1px solid rgba(139, 132, 255, 0.4); border-radius: 20px; font-size: 11px; font-weight: 600; color: #8b84ff; letter-spacing: 2px; margin-bottom: 20px; text-transform: uppercase;">
                                    • AI-POWERED INTELLIGENCE
                                </div>
                                <h1 style="margin: 0 0 15px 0; color: transparent; background: linear-gradient(135deg, #a9a3ff 0%, #d4b3ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 48px; font-weight: 800; font-family: 'Space Grotesk', sans-serif; letter-spacing: -2px;">
                                    Anya
                                </h1>
                                <p style="margin: 0 0 10px 0; color: #b4b4c8; font-size: 18px; font-weight: 500;">
                                    Your AI News Agent — Always On
                                </p>
                                <p style="margin: 0; color: #8a8a9e; font-size: 14px; line-height: 1.6;">
                                    Curated from 85 vetted sources
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Intro -->
                        <tr>
                            <td style="padding: 40px 30px; text-align: center; background: #0d1225;">
                                <p style="margin: 0 0 20px 0; color: #e0e0e8; font-size: 16px; line-height: 1.8;">
                                    Here's your personalized AI news summary. The latest breakthroughs across AI infrastructure, applications, tools and startups.
                                </p>
                                <p style="margin: 0 0 30px 0; color: #8a8a9e; font-size: 14px; line-height: 1.6;">
                                    Curated, synthesized, and delivered. No noise. Just signal.
                                </p>
                                <a href="{app_url}" style="display: inline-block; padding: 14px 28px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 12px; font-weight: 600; font-size: 15px; margin: 10px 0; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);">
                                    🚀 View Full Report
                                </a>
                            </td>
                        </tr>
                        
                        <!-- Categories -->
                        <tr>
                            <td style="padding: 20px 30px 40px 30px; background: #0d1225;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    {category_html}
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background: #0a0e1a; text-align: center; border-top: 1px solid rgba(139, 132, 255, 0.2);">
                                <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 13px;">
                                    Generated on {formatted_date}
                                </p>
                                <p style="margin: 0 0 15px 0; color: #6b7280; font-size: 12px;">
                                    Powered by Anya • Your AI News Agent
                                </p>
                                <a href="{app_url}" style="color: #8b84ff; text-decoration: none; font-size: 14px; font-weight: 600;">
                                    Visit anya-ai-news.railway.app →
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return email_html

@app.route('/send-email', methods=['POST'])
def send_email():
    """Send news summary via email using SendGrid API (no SMTP)."""
    try:
        # Log the request
        print("\n" + "="*60)
        print("EMAIL REQUEST RECEIVED")
        print("="*60)
        
        # Check if request has JSON data
        if not request.is_json:
            print("ERROR: Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        email = data.get('email', '').strip()
        results_data = data.get('results', {})
        
        print(f"Email recipient: {email}")
        print(f"Results data size: {len(str(results_data))} chars")
        
        if not email:
            return jsonify({"error": "Email address is required"}), 400
        
        if not results_data:
            return jsonify({"error": "No results to send"}), 400
        
        # Check for SendGrid API key (preferred method - no SMTP needed)
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        
        if sendgrid_api_key and SENDGRID_AVAILABLE:
            print("Using SendGrid API (no SMTP)")
            try:
                # Generate email HTML
                app_url = request.host_url.rstrip('/')
                email_html = generate_email_html(results_data, app_url)
                print("✓ Email HTML generated")
                
                # Create SendGrid email
                from_email_address = MAIL_FROM or MAIL_USERNAME or "noreply@anya-ai.com"
                from_email = Email(from_email_address, "Anya AI News Agent")
                to_email = To(email)
                subject = "Your AI News Summary from Anya"
                html_content = Content("text/html", email_html)
                
                # Create plain text version as fallback
                plain_text = f"Your AI News Summary from Anya\n\nView the full summary at: {request.host_url}"
                text_content = Content("text/plain", plain_text)
                
                mail_message = SendGridMail(from_email, to_email, subject, text_content)
                mail_message.add_content(html_content)
                
                print(f"From email: {from_email_address}")
                print(f"To email: {email}")
                print(f"Subject: {subject}")
                
                # Send via SendGrid API
                sg = SendGridAPIClient(sendgrid_api_key)
                response = sg.send(mail_message)
                
                print(f"✅ SendGrid response status: {response.status_code}")
                print(f"✅ SendGrid response body: {response.body}")
                print(f"✅ SendGrid response headers: {response.headers}")
                print(f"✅ Email queued successfully to {email} via SendGrid")
                print(f"⚠️ CHECK SENDGRID DASHBOARD for delivery status and any blocks")
                
                # Check for common issues
                if response.status_code == 202:
                    print("✓ Email accepted by SendGrid (202 Accepted)")
                elif response.status_code >= 400:
                    print(f"⚠️ SendGrid returned error status: {response.status_code}")
                
                return jsonify({
                    "success": True,
                    "message": "Email sent successfully! Check your inbox."
                }), 200
                
            except Exception as sg_error:
                print(f"ERROR with SendGrid: {sg_error}")
                import traceback
                print(traceback.format_exc())
                return jsonify({
                    "error": f"SendGrid API error: {str(sg_error)}",
                    "hint": "Check SENDGRID_API_KEY is correct"
                }), 500
        
        # Fallback to SMTP (will likely fail on Railway due to port blocking)
        print("⚠ SendGrid not available, attempting SMTP (may timeout on Railway)")
        
        # Check mail configuration
        print(f"MAIL_USERNAME configured: {bool(MAIL_USERNAME)}")
        print(f"MAIL_PASSWORD configured: {bool(MAIL_PASSWORD)}")
        print(f"Flask-Mail object: {bool(mail)}")
        
        if not MAIL_USERNAME or not MAIL_PASSWORD or mail is None:
            error_msg = "Email service not configured. Please add SENDGRID_API_KEY to Railway environment variables."
            print(f"ERROR: {error_msg}")
            return jsonify({
                "error": error_msg,
                "config_help": "Get free API key from sendgrid.com (100 emails/day free)"
            }), 500
        
        print(f"Using MAIL_USERNAME: {MAIL_USERNAME}")
        print(f"MAIL_SERVER: {MAIL_SERVER}:{MAIL_PORT}")
        print(f"TLS: {MAIL_USE_TLS}")
        print("⚠ WARNING: SMTP connections are often blocked on Railway/cloud platforms")
        
        # Generate email HTML
        try:
            app_url = request.host_url.rstrip('/')
            email_html = generate_email_html(results_data, app_url)
            print("✓ Email HTML generated successfully")
        except Exception as html_error:
            print(f"ERROR generating HTML: {html_error}")
            return jsonify({"error": "Failed to generate email content"}), 500
        
        # Create message
        try:
            msg = Message(
                subject='🤖 Your AI News Summary from Anya',
                recipients=[email],
                html=email_html,
                sender=MAIL_FROM or MAIL_USERNAME
            )
            print("✓ Message object created")
        except Exception as msg_error:
            print(f"ERROR creating message: {msg_error}")
            return jsonify({"error": "Failed to create email message"}), 500
        
        # Send email via SMTP
        print("Attempting to send email via SMTP (this will likely timeout)...")
        try:
            mail.send(msg)
            print(f"✅ Email sent successfully to {email}")
            
            return jsonify({
                "success": True,
                "message": "Email sent successfully! Check your inbox."
            }), 200
            
        except Exception as send_error:
            print(f"ERROR sending email via SMTP: {send_error}")
            import traceback
            print(traceback.format_exc())
            
            # Detailed error messages
            error_str = str(send_error).lower()
            if "timeout" in error_str or "connection" in error_str:
                return jsonify({
                    "error": "SMTP connection blocked by Railway. Please use SendGrid instead.",
                    "solution": "Add SENDGRID_API_KEY environment variable to Railway",
                    "get_key": "Sign up at sendgrid.com for free API key (100 emails/day)"
                }), 500
            elif "authentication" in error_str:
                return jsonify({
                    "error": "Email authentication failed."
                }), 500
            else:
                return jsonify({
                    "error": f"Failed to send email: {str(send_error)}"
                }), 500
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("\n!!! CRITICAL ERROR in send_email route:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Full traceback:")
        print(error_trace)
        print("="*60 + "\n")
        
        return jsonify({
            "error": "Server error while processing email request",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    # Use Railway's PORT environment variable, fallback to 5001 for local development
    PORT = int(os.environ.get('PORT', 5001))
    HOST = os.environ.get('HOST', '0.0.0.0')  # Railway needs 0.0.0.0, not 127.0.0.1
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*60)
    print("🚀 AI News Agent - Web Server")
    print("="*60)
    print(f"\nStarting server on {HOST}:{PORT}")
    print(f"Debug mode: {DEBUG}")
    print(f"OpenAI API Key configured: {'Yes' if os.environ.get('OPENAI_API_KEY') else 'No (will use Fast Mode only)'}")
    print(f"Email configured: {'Yes' if MAIL_USERNAME else 'No'}")
    print("Press Ctrl+C to stop\n")
    print("Health check available at /health")
    print("="*60 + "\n")
    # For Railway, use threaded=True for better performance
    app.run(host=HOST, port=PORT, debug=DEBUG, threaded=True)
