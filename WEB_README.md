# AI News Agent - Web Interface

## 🚀 Quick Start

### Start the Web Server

```bash
cd ~/ai_news_agent

# Option 1: Use the convenience script
./run_server.sh

# Option 2: Run directly
python3 app.py
```

### Access the Interface

Open your web browser and navigate to:
**http://localhost:5001**

> **Note:** Port 5001 is used instead of 5000 to avoid conflicts with macOS AirPlay service.

## Features

### Web Interface
- 🎨 Beautiful, modern UI with gradient design
- 📊 Real-time statistics dashboard
- 📱 Responsive design (works on mobile)
- ⚡ Fast mode (no API key required)
- 🤖 Full mode with AI summaries (requires OpenAI API key)

### Usage

1. **Configure Settings:**
   - **Days to look back**: How many days of articles to fetch (1-30)
   - **Mode:
     - **Fast Mode**: No API key needed, uses RSS summaries
     - **Full Mode**: Requires OpenAI API key, generates AI summaries
   - **Fetch full content**: Optionally fetch full article content (slower)

2. **Click "Run Agent"** and wait for results

3. **View Results:**
   - Statistics dashboard showing total articles and category breakdown
   - Categorized articles with:
     - Article titles (clickable links)
     - Source information
     - Publication dates
     - Summaries (RSS or AI-generated)

## API Endpoint

The web server also exposes a REST API:

### POST /run

Run the agent and get JSON results.

**Request Body:**
```json
{
  "days": 7,
  "mode": "fast",
  "fetchContent": false
}
```

**Response:**
```json
{
  "generated_at": "2024-01-15T10:30:00",
  "categories": {
    "AI Infrastructure": [...],
    "AI Frontier models": [...]
  }
}
```

## Configuration

### Environment Variables

Set these before starting the server for full mode:

```bash
export OPENAI_API_KEY=your_key_here
python3 app.py
```

### Port Configuration

To change the port, edit `app.py`:

```python
PORT = 8080  # Change port here
app.run(host='127.0.0.1', port=PORT, debug=True)
```

## Troubleshooting

**Server won't start?**
- Make sure Flask is installed: `pip3 install flask`
- Check if port 5001 is already in use
- Try a different port in `app.py` (change the `PORT` variable)

**No articles found?**
- Check your internet connection
- Some RSS feeds may be temporarily unavailable
- Try increasing the "days to look back" setting

**API errors?**
- For full mode, ensure `OPENAI_API_KEY` is set
- Check your API key is valid
- Try fast mode if you don't have an API key

## Development

The web interface uses:
- **Flask**: Web framework
- **Vanilla JavaScript**: No external JS dependencies
- **CSS3**: Modern styling with gradients and animations

To modify the UI, edit the `HTML_TEMPLATE` in `app.py`.
