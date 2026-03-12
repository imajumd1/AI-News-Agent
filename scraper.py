"""Web scraper for fetching AI news articles."""

import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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
            # Reduced from max_items * 2 to max_items + 2 for faster processing
            for entry in feed.entries[:max_items + 2]:
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
    
    def _scrape_single_source(self, source_name: str, source_config: Dict, fetch_full_content: bool = False) -> tuple:
        """Scrape a single news source (helper method for parallel execution)."""
        articles = []
        try:
            if source_config["type"] == "rss":
                articles = self.fetch_rss_feed(source_config["url"])
                
                # Optionally enhance articles with full content (slower)
                if fetch_full_content:
                    for article in articles:
                        if article.get("link"):
                            full_content = self.fetch_article_content(article["link"])
                            if full_content:
                                article["full_content"] = full_content
        except Exception as e:
            print(f"✗ {source_name}: Error - {str(e)[:100]}")
            return source_name, []
        
        return source_name, articles
    
    def scrape_all_sources(self, fetch_full_content: bool = False, max_workers: int = 20) -> List[Dict]:
        """Scrape all configured news sources in parallel for 5-10x speed improvement."""
        all_articles = []
        total_sources = len(NEWS_SOURCES)
        
        print(f"\n🚀 Scraping {total_sources} sources in parallel (max {max_workers} workers)...\n")
        start_time = time.time()
        
        # Use ThreadPoolExecutor to scrape multiple sources simultaneously
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all scraping jobs
            future_to_source = {
                executor.submit(self._scrape_single_source, name, config, fetch_full_content): name
                for name, config in NEWS_SOURCES.items()
            }
            
            completed = 0
            # Process results as they complete
            for future in as_completed(future_to_source):
                source_name = future_to_source[future]
                completed += 1
                
                try:
                    source_name, articles = future.result(timeout=REQUEST_TIMEOUT + 5)
                    all_articles.extend(articles)
                    print(f"[{completed}/{total_sources}] ✓ {source_name}: {len(articles)} articles")
                except Exception as e:
                    print(f"[{completed}/{total_sources}] ✗ {source_name}: {str(e)[:100]}")
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ Scraping complete! {len(all_articles)} total articles in {elapsed_time:.1f}s\n")
        
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
