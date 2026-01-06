"""Configuration settings for the AI News Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# News Sources Configuration - Comprehensive AI News Coverage
NEWS_SOURCES = {
    # Tech Publications
    "techcrunch_ai": {
        "url": "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "type": "rss"
    },
    "the_verge_ai": {
        "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "type": "rss"
    },
    "wired_ai": {
        "url": "https://www.wired.com/feed/tag/artificial-intelligence/latest/rss",
        "type": "rss"
    },
    "mit_tech_review": {
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
        "type": "rss"
    },
    "venturebeat_ai": {
        "url": "https://venturebeat.com/ai/feed/",
        "type": "rss"
    },
    "zdnet_ai": {
        "url": "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
        "type": "rss"
    },
    "arstechnica_ai": {
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "type": "rss"
    },
    "engadget_ai": {
        "url": "https://www.engadget.com/rss.xml",
        "type": "rss"
    },
    
    # AI-Specific Blogs & Sites
    "hacker_news": {
        "url": "https://hnrss.org/newest?q=AI",
        "type": "rss"
    },
    "arxiv_ai": {
        "url": "http://arxiv.org/rss/cs.AI",
        "type": "rss"
    },
    "arxiv_ml": {
        "url": "http://arxiv.org/rss/cs.LG",
        "type": "rss"
    },
    "towards_data_science": {
        "url": "https://towardsdatascience.com/feed",
        "type": "rss"
    },
    "ai_news": {
        "url": "https://www.artificialintelligence-news.com/feed/",
        "type": "rss"
    },
    "synced_review": {
        "url": "https://syncedreview.com/feed/",
        "type": "rss"
    },
    "the_batch": {
        "url": "https://www.deeplearning.ai/the-batch/feed/",
        "type": "rss"
    },
    
    # Major Newspapers - Tech Sections
    "nytimes_tech": {
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "type": "rss"
    },
    "washington_post_tech": {
        "url": "https://feeds.washingtonpost.com/rss/business/technology",
        "type": "rss"
    },
    "guardian_tech": {
        "url": "https://www.theguardian.com/technology/artificialintelligenceai/rss",
        "type": "rss"
    },
    "bbc_tech": {
        "url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "type": "rss"
    },
    "reuters_tech": {
        "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
        "type": "rss"
    },
    
    # Industry & Business
    "bloomberg_tech": {
        "url": "https://www.bloomberg.com/feed/topics/technology",
        "type": "rss"
    },
    "wsj_tech": {
        "url": "https://feeds.a.dj.com/rss/RSSWSJD.xml",
        "type": "rss"
    },
    "forbes_ai": {
        "url": "https://www.forbes.com/innovation/feed2/",
        "type": "rss"
    },
    "cnbc_tech": {
        "url": "https://www.cnbc.com/id/19854910/device/rss/rss.html",
        "type": "rss"
    },
    
    # Research & Academic
    "nature_ai": {
        "url": "https://www.nature.com/subjects/artificial-intelligence.rss",
        "type": "rss"
    },
    "science_daily_ai": {
        "url": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
        "type": "rss"
    },
    "ieee_spectrum": {
        "url": "https://spectrum.ieee.org/rss/blog/artificial-intelligence/fulltext",
        "type": "rss"
    },
    
    # Developer & Technical
    "github_blog": {
        "url": "https://github.blog/feed/",
        "type": "rss"
    },
    "google_ai_blog": {
        "url": "https://ai.googleblog.com/feeds/posts/default",
        "type": "rss"
    },
    "openai_blog": {
        "url": "https://openai.com/blog/rss.xml",
        "type": "rss"
    },
    "anthropic_blog": {
        "url": "https://www.anthropic.com/index.xml",
        "type": "rss"
    }
}

# Category Keywords
CATEGORY_KEYWORDS = {
    "AI Infrastructure": [
        "infrastructure", "compute", "gpu", "datacenter", "cloud", "training infrastructure",
        "hardware", "chips", "processors", "servers", "distributed training", "scaling",
        "mlops", "deployment", "inference", "serving", "kubernetes", "orchestration",
        "data pipeline", "storage", "networking", "optimization", "efficiency", "compute cluster"
    ],
    "AI Frontier models": [
        "frontier model", "large language model", "llm", "gpt", "claude", "gemini",
        "multimodal", "foundation model", "general intelligence", "agi", "reasoning",
        "capabilities", "benchmark", "evaluation", "safety", "alignment", "scaling laws",
        "emergent", "breakthrough", "state-of-the-art", "sota", "performance", "parameters"
    ],
    "AI Builder tools": [
        "developer tool", "sdk", "api", "framework", "library", "platform", "toolkit",
        "development", "programming", "code", "software", "build", "create", "tool",
        "ide", "editor", "assistant", "copilot", "autocomplete", "generation", "studio"
    ],
    "AI startups to watch": [
        "startup", "funding", "raise", "series a", "series b", "seed", "venture", "capital",
        "unicorn", "valuation", "ipo", "acquisition", "merger", "new company", "launch",
        "announcement", "backed", "investor", "accelerator", "incubator"
    ]
}

# Scraping Configuration
MAX_ARTICLES_PER_SOURCE = 3  # Reduced per source since we have many sources now
REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
RATE_LIMIT_DELAY = 0.3  # Delay between sources in seconds