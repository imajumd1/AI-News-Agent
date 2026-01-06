# AI News Agent - MVP Version

## 🌐 Web Interface (Recommended)

Run the agent with a beautiful web interface on localhost:

```bash
cd ~/ai_news_agent
./run_server.sh
# Or: python3 app.py
```

Then open your browser to: **http://localhost:5001**

> **Note:** Port 5001 is used to avoid conflicts with macOS AirPlay service.

## Quick Start (No API Key Required)

The MVP version can run in **fast mode** without requiring an OpenAI API key. This mode:
- ✅ Scrapes RSS feeds for AI news
- ✅ Categorizes articles automatically
- ✅ Uses RSS summaries (no full content scraping)
- ❌ Skips AI-generated summaries (uses RSS summaries instead)

### Setup (First Time Only):

```bash
cd ~/ai_news_agent

# Run the setup script
./setup.sh

# Or manually install dependencies
pip3 install -r requirements.txt
```

### Run MVP:

```bash
# Fast mode (no API key needed)
python3 main.py --fast

# Or use the convenience script
./run_mvp.sh
```

## Full Version (With AI Summaries)

For AI-powered summaries, you'll need an OpenAI API key:

```bash
# Set your API key
export OPENAI_API_KEY=your_key_here

# Run with full features
python3 main.py
```

## MVP Features

### Command Line Options

```bash
# Fast mode (MVP - no API key needed)
python3 main.py --fast

# Fast mode with custom days
python3 main.py --fast --days 3

# Skip summaries but fetch full content
python3 main.py --no-summaries

# Full version with all features
python3 main.py --days 7
```

### What the MVP Does

1. **Scrapes** RSS feeds from:
   - Hacker News (AI topics)
   - arXiv (AI research)
   - TechCrunch AI
   - VentureBeat AI

2. **Categorizes** articles into:
   - AI Infrastructure
   - AI Frontier models

3. **Displays** results with:
   - Article titles
   - Sources
   - Links
   - RSS summaries (in fast mode)
   - AI summaries (in full mode)

## Example Output

```
================================================================================
AI NEWS SUMMARY REPORT
Generated: 2024-01-15 10:30:00
================================================================================

================================================================================
CATEGORY: AI INFRASTRUCTURE
================================================================================

[1] New GPU Cluster for AI Training
    Source: TechCrunch
    Link: https://techcrunch.com/...
    Published: 1 days ago

    Summary: TechCrunch reports on a new GPU cluster designed for...

[2] MLOps Platform Update
    Source: VentureBeat
    Link: https://venturebeat.com/...
    Published: 2 days ago

    Summary: Latest updates to MLOps deployment platform...
```

## Next Steps

1. **Test the MVP**: Run `python3 main.py --fast` to see it in action
2. **Add API Key**: For AI summaries, set `OPENAI_API_KEY` and run without `--fast`
3. **Customize**: Edit `config.py` to add more sources or adjust keywords

## Project Structure

```
ai_news_agent/
├── main.py              # Entry point
├── agent.py             # Main orchestrator
├── scraper.py           # Web scraping
├── categorizer.py       # Article categorization
├── summarizer.py        # AI summarization
├── config.py            # Configuration
├── requirements.txt      # Dependencies
├── setup.sh             # Setup script
├── run_mvp.sh           # Quick MVP runner
├── README.md            # Full documentation
└── MVP_README.md         # This file
```

## Troubleshooting

**No articles found?**
- Check your internet connection
- Try increasing `--days` parameter
- Some RSS feeds may be temporarily unavailable

**Want faster results?**
- Use `--fast` mode
- Reduce `MAX_ARTICLES_PER_SOURCE` in `config.py`
- Use `--days 3` for fewer articles
