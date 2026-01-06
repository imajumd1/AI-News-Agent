# AI News Agent

An intelligent agent that scrapes the web for the latest AI developments and generates summaries across two key categories:
- **AI Infrastructure**: Hardware, compute, deployment, MLOps, and infrastructure-related news
- **AI Frontier models**: Large language models, breakthrough capabilities, and state-of-the-art research

## Features

- 🔍 **Multi-source scraping**: Aggregates news from Hacker News, arXiv, TechCrunch, and VentureBeat
- 🏷️ **Intelligent categorization**: Automatically classifies articles into relevant categories
- 📝 **AI-powered summaries**: Generates concise, informative summaries using OpenAI's API
- 📊 **Recent articles only**: Filters to show only articles from the last 7 days (configurable)
- 💾 **Export to JSON**: Saves results for further analysis

## Setup

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Navigate to the project directory:
```bash
cd ~/ai_news_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

Or export it as an environment variable:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

Run the agent with default settings (last 7 days):
```bash
python main.py
```

### Advanced Usage

```bash
# Look back 14 days
python main.py --days 14

# Specify output file
python main.py --output my_report.json

# Don't save to file (only display)
python main.py --no-save
```

## Configuration

Edit `config.py` to customize:

- **News sources**: Add or modify RSS feeds in `NEWS_SOURCES`
- **Category keywords**: Adjust keywords for better categorization
- **API settings**: Change OpenAI model or endpoint
- **Scraping limits**: Adjust `MAX_ARTICLES_PER_SOURCE`

## Output

The agent provides:

1. **Console output**: Formatted report with all articles and summaries
2. **JSON file**: Structured data saved to `ai_news_report_YYYYMMDD_HHMMSS.json`

### Example Output Structure

```json
{
  "generated_at": "2024-01-15T10:30:00",
  "categories": {
    "AI Infrastructure": [
      {
        "title": "New GPU Cluster for AI Training",
        "source": "TechCrunch",
        "link": "https://...",
        "published": "2024-01-14",
        "days_ago": 1,
        "ai_summary": "TechCrunch reports on a new GPU cluster..."
      }
    ],
    "AI Frontier models": [...]
  }
}
```

## Architecture

- **`scraper.py`**: Handles web scraping from RSS feeds and article content extraction
- **`categorizer.py`**: Categorizes articles based on keyword matching
- **`summarizer.py`**: Uses OpenAI API to generate article summaries
- **`agent.py`**: Orchestrates the complete pipeline
- **`main.py`**: CLI interface and entry point
- **`config.py`**: Configuration settings

## Notes

- The agent respects rate limits and includes delays between requests
- Article content is limited to 5000 characters for efficiency
- Summaries are generated using GPT-4o-mini by default (configurable)
- Uncategorized articles are logged but not included in the final report

## Troubleshooting

**Error: OPENAI_API_KEY not set**
- Make sure you've set the API key in `.env` or as an environment variable

**No articles found**
- Check your internet connection
- Verify RSS feed URLs in `config.py` are still valid
- Try increasing the `--days` parameter

**Rate limiting errors**
- The agent includes delays, but if you encounter rate limits, increase delays in `scraper.py`

## License

MIT License - feel free to modify and use as needed.
