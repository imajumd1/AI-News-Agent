#!/usr/bin/env python3
"""Web application for AI News Agent."""

from flask import Flask, render_template_string, request, jsonify
from agent import AINewsAgent
import json
from datetime import datetime
import os
import html

app = Flask(__name__)

# Enable CORS manually (for localhost, CORS isn't strictly needed, but helps)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Category configuration with icons and colors
CATEGORY_CONFIG = {
    "AI Infrastructure": {
        "icon": "🏗️",
        "color": "#667eea",
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    "AI Frontier models": {
        "icon": "🚀",
        "color": "#f093fb",
        "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    },
    "AI Builder tools": {
        "icon": "🛠️",
        "color": "#4facfe",
        "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
    },
    "AI startups to watch": {
        "icon": "⭐",
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        .controls {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 30px;
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
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 40px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            white-space: nowrap;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        .btn:active {
            transform: translateY(0);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 60px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 30px;
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
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
            transition: all 0.3s;
            cursor: pointer;
            border: 3px solid transparent;
        }
        .category-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }
        .category-box.expanded {
            border-color: currentColor;
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
            font-size: 0.9em;
            color: #666;
            position: relative;
            z-index: 1;
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
            line-height: 2;
            color: #444;
            font-size: 1.05em;
            font-weight: 400;
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
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 12px;
            border-left: 4px solid;
            transition: all 0.3s;
        }
        .article-card:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .article-title {
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.4;
        }
        .article-title a {
            color: inherit;
            text-decoration: none;
        }
        .article-title a:hover {
            text-decoration: underline;
        }
        .article-meta {
            color: #666;
            font-size: 0.85em;
            margin-bottom: 12px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .article-summary {
            color: #555;
            line-height: 1.7;
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
            <h1>🤖 AI News Agent</h1>
            <p>Stay updated with the latest AI developments</p>
        </div>

        <div class="controls">
            <div class="form-group">
                <label for="days">Days to look back</label>
                <input type="number" id="days" name="days" value="7" min="1" max="30">
            </div>
            <div class="form-group">
                <label for="mode">Mode</label>
                <select id="mode" name="mode">
                    <option value="fast">Fast Mode (RSS summaries)</option>
                    <option value="full">Full Mode (AI summaries)</option>
                </select>
            </div>
            <div class="form-group">
                <button type="button" class="btn" id="submitBtn" onclick="runAgent()">Fetch Latest News</button>
            </div>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="font-size: 1.1em; margin-top: 20px;">Scraping news sources and generating summaries...</p>
            <p style="color: #666; font-size: 0.9em; margin-top: 10px;">This may take a minute or two</p>
        </div>

        <div id="errorContainer"></div>

        <div class="results" id="results">
            <div class="categories-grid" id="categoriesGrid"></div>
        </div>
    </div>

    <script>
        const categoryConfig = {
            "AI Infrastructure": { icon: "🏗️", color: "#667eea" },
            "AI Frontier models": { icon: "🚀", color: "#f093fb" },
            "AI Builder tools": { icon: "🛠️", color: "#4facfe" },
            "AI startups to watch": { icon: "⭐", color: "#fa709a" }
        };

        async function runAgent() {
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const errorContainer = document.getElementById('errorContainer');
            const categoriesGrid = document.getElementById('categoriesGrid');
            
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
            loadingText.textContent = 'Scraping 31 sources... This may take 40-60 seconds. Please wait...';
            
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
        
        function displayResults(data) {
            console.log('displayResults called with:', data);
            const results = document.getElementById('results');
            const categoriesGrid = document.getElementById('categoriesGrid');
            
            // Clear previous results
            categoriesGrid.innerHTML = '';
            
            // Create category boxes
            const categoryOrder = [
                "AI Infrastructure",
                "AI Frontier models", 
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
                    // Category Overview Section - Show FIRST and prominently
                    const overviewDiv = document.createElement('div');
                    overviewDiv.className = 'category-overview';
                    overviewDiv.style.borderLeftColor = config.color;
                    if (categorySummary) {
                        overviewDiv.innerHTML = `
                            <div class="category-overview-title">
                                <span>📊</span>
                                <span>AI-Generated Category Summary</span>
                            </div>
                            <div class="category-overview-text">${escapeHtml(categorySummary)}</div>
                        `;
                    } else {
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
                    content.appendChild(articlesSection);
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
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Render the main page."""
    return render_template_string(HTML_TEMPLATE)

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
            "AI Infrastructure": [],
            "AI Frontier models": [],
            "AI Builder tools": [],
            "AI startups to watch": []
        }
        
        # Prepare response
        response_data = {
            "generated_at": datetime.now().isoformat(),
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

if __name__ == '__main__':
    PORT = 5001
    print("\n" + "="*60)
    print("🚀 AI News Agent - Web Server")
    print("="*60)
    print(f"\nStarting server on http://localhost:{PORT}")
    print("Press Ctrl+C to stop\n")
    app.run(host='127.0.0.1', port=PORT, debug=True)
