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

try:
    from config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM
    print("✓ Config imported successfully")
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
        "icon": "🖥️",
        "color": "#667eea",
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    "AI Applications": {
        "icon": "🤖",
        "color": "#4facfe",
        "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
    },
    "AI Builder tools": {
        "icon": "🧠",
        "color": "#f093fb",
        "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    },
    "AI startups to watch": {
        "icon": "🚀",
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
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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
        }
        .header {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 60px 40px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 100px rgba(102, 126, 234, 0.2);
            margin-bottom: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
            animation: glow 8s ease-in-out infinite;
        }
        @keyframes glow {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(20px, 20px); }
        }
        .header h1 {
            color: #ffffff;
            margin-bottom: 15px;
            font-size: 3.5em;
            font-weight: 800;
            position: relative;
            z-index: 1;
            text-shadow: 0 0 30px rgba(102, 126, 234, 0.5), 0 0 60px rgba(102, 126, 234, 0.3);
            letter-spacing: -1px;
        }
        .header h1 .robot-icon {
            display: inline-block;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        .header p {
            color: #b4b4c8;
            font-size: 1.3em;
            position: relative;
            z-index: 1;
            font-weight: 400;
        }
        .live-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 15px;
            padding: 8px 16px;
            background: rgba(76, 175, 80, 0.15);
            border: 1px solid rgba(76, 175, 80, 0.3);
            border-radius: 20px;
            font-size: 0.9em;
            color: #4caf50;
        }
        .live-dot {
            width: 8px;
            height: 8px;
            background: #4caf50;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.2); }
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
            font-size: 3em;
            margin-bottom: 15px;
            position: relative;
            z-index: 1;
        }
        .category-title {
            font-size: 1.4em;
            font-weight: 700;
            color: #333;
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
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .category-overview-text {
            line-height: 1.8;
            color: #444;
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
            background-color: #fefefe;
            margin: 5% auto;
            padding: 30px;
            border: 1px solid #888;
            border-radius: 15px;
            width: 80%;
            max-width: 700px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
        }
        .modal-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #333;
        }
        .close-modal {
            color: #aaa;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            line-height: 1;
        }
        .close-modal:hover,
        .close-modal:focus {
            color: #000;
        }
        .modal-body {
            line-height: 1.8;
            color: #444;
            font-size: 1.05em;
        }
        .articles-section {
            margin-top: 20px;
        }
        .articles-toggle {
            padding: 15px 20px;
            background: #f8f9fa;
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
            background: #e9ecef;
            border-color: currentColor;
        }
        .articles-toggle-title {
            font-weight: 600;
            color: #333;
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
            color: #999;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 4px solid #c33;
        }
        .results {
            display: none;
        }
        .results.visible {
            display: block;
        }
        .email-section {
            margin-top: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-radius: 15px;
            border: 2px solid #667eea;
        }
        .email-title {
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 20px;
            color: #333;
        }
        .email-form {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
        }
        .email-input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        .email-input:focus {
            outline: none;
            border-color: #667eea;
        }
        .email-send-btn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .email-send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .email-send-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .email-message {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            display: none;
        }
        .email-message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .email-message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .feedback-section {
            margin-top: 40px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
            border: 2px solid #e0e0e0;
        }
        .feedback-title {
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 20px;
            color: #333;
        }
        .feedback-buttons {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .feedback-btn {
            flex: 1;
            padding: 15px 30px;
            border: 2px solid #ddd;
            border-radius: 10px;
            background: white;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .feedback-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .feedback-btn.thumbs-up {
            border-color: #4caf50;
            color: #4caf50;
        }
        .feedback-btn.thumbs-up:hover,
        .feedback-btn.thumbs-up.active {
            background: #4caf50;
            color: white;
        }
        .feedback-btn.thumbs-down {
            border-color: #f44336;
            color: #f44336;
        }
        .feedback-btn.thumbs-down:hover,
        .feedback-btn.thumbs-down.active {
            background: #f44336;
            color: white;
        }
        .feedback-comment {
            margin-top: 20px;
        }
        .feedback-comment textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            min-height: 100px;
            box-sizing: border-box;
        }
        .feedback-comment textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .feedback-submit {
            margin-top: 15px;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        .feedback-submit:hover {
            background: #5568d3;
        }
        .feedback-submit:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .feedback-message {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            display: none;
        }
        .feedback-message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .feedback-message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
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
        <div class="header">
            <h1><span class="robot-icon">🤖</span> Anya - Your AI News Agent</h1>
            <p>Stay updated with the latest breakthroughs in AI, infrastructure, and startups</p>
            <div class="live-indicator">
                <div class="live-dot"></div>
                <span>Scanning 54 sources in real-time</span>
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
            <p style="font-size: 1.1em; margin-top: 20px;">Scraping 54 sources to get you the most relevant and current AI news. This may take a minute or two. Please wait...</p>
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
            
            <!-- Email Section -->
            <div class="email-section" id="emailSection" style="display: none;">
                <div class="email-title">📧 Send Summary via Email</div>
                <div class="email-form">
                    <input type="email" id="emailInput" placeholder="Enter your email address" class="email-input">
                    <button class="email-send-btn" id="emailSendBtn" onclick="sendEmail()">Send Email</button>
                </div>
                <div class="email-message" id="emailMessage"></div>
            </div>
            
            <!-- Feedback Section -->
            <div class="feedback-section" id="feedbackSection" style="display: none;">
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
            "GPU and AI Infra": { icon: "🖥️", color: "#667eea" },
            "AI Applications": { icon: "🤖", color: "#4facfe" },
            "AI Builder tools": { icon: "🧠", color: "#f093fb" },
            "AI startups to watch": { icon: "🚀", color: "#fa709a" }
        };

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
            submitBtn.textContent = 'Scraping...';
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
            loadingText.textContent = 'Scraping 54 sources to get you the most relevant and current AI news. This may take a minute or two. Please wait...';
            
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
            
            // Show email and feedback sections after results are displayed
            const emailSection = document.getElementById('emailSection');
            if (emailSection) {
                emailSection.style.display = 'block';
            }
            
            const feedbackSection = document.getElementById('feedbackSection');
            if (feedbackSection) {
                feedbackSection.style.display = 'block';
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
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    messageDiv.className = 'email-message success';
                    messageDiv.textContent = '✅ Email sent successfully! Check your inbox.';
                    messageDiv.style.display = 'block';
                    emailInput.value = '';
                } else {
                    throw new Error(data.error || 'Failed to send email');
                }
            } catch (error) {
                messageDiv.className = 'email-message error';
                messageDiv.textContent = `❌ Error: ${error.message}. Please check email configuration.`;
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
        "GPU and AI Infra": {"icon": "🏗️", "color": "#667eea"},
        "AI Applications": {"icon": "🚀", "color": "#f093fb"},
        "AI Builder tools": {"icon": "🛠️", "color": "#4facfe"},
        "AI startups to watch": {"icon": "⭐", "color": "#fa709a"}
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
            <td style="padding: 30px; background: linear-gradient(135deg, {config['color']}15 0%, {config['color']}25 100%); border-radius: 15px; margin-bottom: 20px;">
                <h2 style="margin: 0 0 15px 0; color: {config['color']}; font-size: 24px;">
                    {config['icon']} {category_name}
                </h2>
                {f'<p style="color: #555; line-height: 1.6; margin-bottom: 20px; font-size: 16px;">{html.escape(summary_preview)}</p>' if summary_preview else ''}
                <p style="color: #666; margin: 10px 0; font-weight: 600;">📰 {len(articles)} Article{'' if len(articles) == 1 else 's'}</p>
                <ul style="list-style: none; padding: 0; margin: 15px 0;">
        """
        
        for article in articles[:5]:  # Show top 5 articles
            title = article.get('title', 'No title')
            link = article.get('link', '#')
            source = article.get('source', 'Unknown')
            category_html += f"""
                    <li style="margin-bottom: 15px; padding: 15px; background: white; border-radius: 8px; border-left: 4px solid {config['color']};">
                        <a href="{link}" style="color: {config['color']}; text-decoration: none; font-weight: 600; font-size: 16px; display: block; margin-bottom: 5px;">
                            {html.escape(title)}
                        </a>
                        <span style="color: #999; font-size: 14px;">Source: {html.escape(source)}</span>
                    </li>
            """
        
        if len(articles) > 5:
            category_html += f"""
                    <li style="text-align: center; margin-top: 10px;">
                        <span style="color: #999; font-size: 14px;">... and {len(articles) - 5} more articles</span>
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
        <title>AI News Summary</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 40px 0;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                                <h1 style="margin: 0; color: white; font-size: 32px; font-weight: 700;">
                                    🤖 AI News Summary
                                </h1>
                                <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px;">
                                    Your curated AI news digest
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Intro -->
                        <tr>
                            <td style="padding: 40px 30px; text-align: center; background: white;">
                                <p style="margin: 0 0 20px 0; color: #333; font-size: 18px; line-height: 1.6;">
                                    Hello! 👋
                                </p>
                                <p style="margin: 0 0 30px 0; color: #666; font-size: 16px; line-height: 1.8;">
                                    Here's your personalized AI news summary, curated from 54+ trusted sources. 
                                    Stay ahead of the latest developments in AI infrastructure, AI applications, 
                                    builder tools, and startups to watch.
                                </p>
                                <a href="{app_url}" style="display: inline-block; padding: 14px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; font-size: 16px; margin: 10px 0;">
                                    🚀 View Full Report
                                </a>
                            </td>
                        </tr>
                        
                        <!-- Categories -->
                        <tr>
                            <td style="padding: 30px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    {category_html}
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px; background: #f8f9fa; text-align: center; border-top: 2px solid #e0e0e0;">
                                <p style="margin: 0 0 10px 0; color: #999; font-size: 14px;">
                                    Generated on {formatted_date}
                                </p>
                                <p style="margin: 0; color: #999; font-size: 12px;">
                                    This summary was generated by the AI News Agent
                                </p>
                                <p style="margin: 15px 0 0 0;">
                                    <a href="{app_url}" style="color: #667eea; text-decoration: none; font-size: 14px; font-weight: 600;">
                                        Visit AI News Agent →
                                    </a>
                                </p>
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
    """Send news summary via email."""
    try:
        data = request.json
        email = data.get('email', '').strip()
        results_data = data.get('results', {})
        
        if not email:
            return jsonify({"error": "Email address is required"}), 400
        
        if not MAIL_USERNAME or not MAIL_PASSWORD or mail is None:
            return jsonify({
                "error": "Email not configured. Please set MAIL_USERNAME and MAIL_PASSWORD in .env file.",
                "config_help": "Add to .env: MAIL_USERNAME=your_email@gmail.com, MAIL_PASSWORD=your_app_password"
            }), 500
        
        if not results_data:
            return jsonify({"error": "No results to send"}), 400
        
        print(f"Attempting to send email to: {email}")
        print(f"Using MAIL_USERNAME: {MAIL_USERNAME}")
        print(f"MAIL_SERVER: {MAIL_SERVER}:{MAIL_PORT}")
        
        # Generate email HTML
        app_url = request.host_url.rstrip('/')
        email_html = generate_email_html(results_data, app_url)
        
        # Create message
        msg = Message(
            subject='🤖 Your AI News Summary',
            recipients=[email],
            html=email_html,
            sender=MAIL_FROM or MAIL_USERNAME
        )
        
        print(f"Message created, attempting to send via Flask-Mail...")
        
        # Send email
        mail.send(msg)
        
        print(f"✓ Email sent successfully to {email}")
        
        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"!!! ERROR sending email: {e}")
        print(f"Error type: {type(e).__name__}")
        print(error_trace)
        
        # Return user-friendly error messages
        error_msg = str(e)
        if "authentication" in error_msg.lower() or "username" in error_msg.lower():
            error_msg = "Email authentication failed. Please check MAIL_USERNAME and MAIL_PASSWORD are correct. Use Gmail App Password, not regular password."
        elif "connection" in error_msg.lower() or "refused" in error_msg.lower():
            error_msg = "Could not connect to email server. Please check MAIL_SERVER and MAIL_PORT settings."
        
        return jsonify({
            "error": error_msg,
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
