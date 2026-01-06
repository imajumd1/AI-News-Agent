"""Web scraper for fetching AI news articles."""

import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import time
from config import NEWS_SOURCES, REQUEST_TIMEOUT, USER_AGENT, MAX_ARTICLES_PER_SOURCE, RATE_LIMIT_DELAY


class NewsScraper:
    """Scrapes news articles from various sources."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
    
    def fetch_rss_feed(self, url: str, max_items: int = MAX_ARTICLES_PER_SOURCE) -> List[Dict]:
        """Fetch and parse RSS feed."""
        articles = []
        try:
            feed = feedparser.parse(url)
            # Filter for AI-related content if feed is general
            for entry in feed.entries[:max_items * 2]:  # Get more to filter
                title = entry.get("title", "").lower()
                summary = entry.get("summary", "").lower()
                
                # Basic AI keyword filter for general feeds
                ai_keywords = ["ai", "artificial intelligence", "machine learning", "ml", "llm", 
                              "neural", "deep learning", "gpt", "claude", "gemini", "openai",
                              "anthropic", "transformer", "model", "algorithm"]
                
                # For general feeds, check if content is AI-related
                is_ai_related = any(keyword in title or keyword in summary for keyword in ai_keywords)
                
                # Always include if from AI-specific sources or if AI-related
                if is_ai_related or len(articles) < max_items:
                    article = {
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "summary": entry.get("summary", ""),
                        "source": feed.feed.get("title", "Unknown"),
                    }
                    articles.append(article)
                    if len(articles) >= max_items:
                        break
        except Exception as e:
            print(f"  ⚠️  Error fetching RSS feed {url}: {str(e)[:100]}")
        return articles
    
    def fetch_article_content(self, url: str) -> Optional[str]:
        """Fetch full article content from URL."""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Try to find main content
            content_selectors = [
                "article",
                ".article-content",
                ".post-content",
                ".entry-content",
                "main",
                ".content"
            ]
            
            content = None
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(separator=" ", strip=True)
                    break
            
            # Fallback to body if no specific content found
            if not content:
                body = soup.find("body")
                if body:
                    content = body.get_text(separator=" ", strip=True)
            
            # Clean up content
            if content:
                content = " ".join(content.split())
                # Limit content length
                if len(content) > 5000:
                    content = content[:5000] + "..."
            
            return content
        except Exception as e:
            print(f"Error fetching article content from {url}: {e}")
            return None
    
    def scrape_all_sources(self, fetch_full_content: bool = False) -> List[Dict]:
        """Scrape all configured news sources."""
        all_articles = []
        
        total_sources = len(NEWS_SOURCES)
        current_source = 0
        
        for source_name, source_config in NEWS_SOURCES.items():
            current_source += 1
            print(f"[{current_source}/{total_sources}] Scraping {source_name}...", end=" ")
            
            if source_config["type"] == "rss":
                articles = self.fetch_rss_feed(source_config["url"])
                
                # Optionally enhance articles with full content (slower)
                if fetch_full_content:
                    for article in articles:
                        if article.get("link"):
                            print(f"  Fetching content for: {article['title'][:50]}...")
                            full_content = self.fetch_article_content(article["link"])
                            if full_content:
                                article["full_content"] = full_content
                            time.sleep(0.3)  # Be respectful with requests
                
                all_articles.extend(articles)
                print(f"✓ {len(articles)} articles")
            
            time.sleep(RATE_LIMIT_DELAY)  # Rate limiting between sources
        
        return all_articles
    
    def filter_recent_articles(self, articles: List[Dict], days: int = 7) -> List[Dict]:
        """Filter articles to only include recent ones."""
        from dateparser import parse as parse_date
        
        recent_articles = []
        cutoff_date = datetime.now()
        
        for article in articles:
            published_str = article.get("published", "")
            if published_str:
                try:
                    published_date = parse_date(published_str)
                    if published_date:
                        days_ago = (cutoff_date - published_date.replace(tzinfo=None)).days
                        if days_ago <= days:
                            article["days_ago"] = days_ago
                            recent_articles.append(article)
                except Exception:
                    # If date parsing fails, include the article anyway
                    recent_articles.append(article)
            else:
                # If no date, include it
                recent_articles.append(article)
        
        return recent_articles
