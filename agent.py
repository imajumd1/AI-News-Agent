"""Main agent orchestrator for AI news scraping and summarization."""

from typing import Dict, List
from scraper import NewsScraper
from categorizer import ArticleCategorizer
from summarizer import ArticleSummarizer
from startup_fetcher import StartupFetcher
from datetime import datetime
import json


class AINewsAgent:
    """Main agent that orchestrates scraping, categorization, and summarization."""
    
    def __init__(self):
        self.scraper = NewsScraper()
        self.categorizer = ArticleCategorizer()
        self.summarizer = ArticleSummarizer()
        self.startup_fetcher = StartupFetcher()
    
    def run(self, days: int = 7, fetch_full_content: bool = False, generate_summaries: bool = True) -> Dict[str, List[Dict]]:
        """Run the complete pipeline."""
        print("=" * 60)
        print("AI News Agent - Scraping Latest Developments")
        print("=" * 60)
        print()
        
        # Step 1: Scrape articles
        print("Step 1: Scraping news sources...")
        articles = self.scraper.scrape_all_sources(fetch_full_content=fetch_full_content)
        print(f"Found {len(articles)} total articles")
        print()
        
        # Step 2: Filter recent articles
        print("Step 2: Filtering recent articles...")
        recent_articles = self.scraper.filter_recent_articles(articles, days=days)
        print(f"Found {len(recent_articles)} articles from the last {days} days")
        print()
        
        # Step 3: Categorize articles
        print("Step 3: Categorizing articles...")
        categorized, uncategorized = self.categorizer.categorize_articles(recent_articles)
        
        for category, articles in categorized.items():
            print(f"  {category}: {len(articles)} articles")
        print(f"  Uncategorized: {len(uncategorized)} articles")
        print()
        
        # Step 4: Generate summaries (optional)
        # Ensure all categories are present
        results = {
            "AI Infrastructure": [],
            "AI Frontier models": [],
            "AI Builder tools": [],
            "AI startups to watch": []
        }
        
        # Special handling for "AI startups to watch" category
        startups_category = "AI startups to watch"
        print(f"\nStep 4a: Fetching top AI enterprise startups for '{startups_category}'...")
        startup_items, startup_summary = self.startup_fetcher.fetch_startups()
        
        # Merge startups with any articles already categorized as startups
        if startups_category in categorized:
            startup_items = startup_items + categorized[startups_category]
        
        if generate_summaries:
            print("Step 4: Generating summaries...")
            for category, articles in categorized.items():
                # Skip startups category - we'll handle it separately
                if category == startups_category:
                    continue
                    
                if articles:
                    print(f"\nProcessing {category} ({len(articles)} articles)...")
                    # Generate category-level summary first
                    category_summary = None
                    if hasattr(self.summarizer, 'generate_category_summary') and self.summarizer.client:
                        print(f"  Generating category overview...")
                        try:
                            category_summary = self.summarizer.generate_category_summary(articles, category)
                            if category_summary:
                                print(f"  ✓ Category summary generated ({len(category_summary)} chars)")
                            else:
                                print(f"  ⚠ Category summary returned None (API may have failed)")
                        except Exception as e:
                            print(f"  ⚠ Could not generate category summary: {str(e)[:100]}")
                    elif not self.summarizer.client:
                        print(f"  ⚠ Skipping category summary - OpenAI API key not configured")
                    else:
                        print(f"  ⚠ Category summary method not available")
                    
                    # Generate individual article summaries
                    # Even if summarization fails, we still want the articles
                    try:
                        summarized = self.summarizer.generate_summaries(articles, category)
                    except Exception as e:
                        print(f"  Warning: Summarization failed, using original articles: {e}")
                        summarized = articles
                    
                    # Add category summary to results
                    for article in summarized:
                        article["category_summary"] = category_summary
                    
                    results[category] = summarized
                else:
                    results[category] = []
            
            # Handle startups category separately
            print(f"\nProcessing {startups_category} ({len(startup_items)} items)...")
            # Add category summary to all startup items
            for startup in startup_items:
                startup["category_summary"] = startup_summary
            results[startups_category] = startup_items
        else:
            # Just return categorized articles without summaries
            for category in results.keys():
                if category == startups_category:
                    results[category] = startup_items
                else:
                    results[category] = categorized.get(category, [])
        
        print()
        print("=" * 60)
        print("Processing Complete!")
        print("=" * 60)
        
        return results
    
    def format_output(self, results: Dict[str, List[Dict]]) -> str:
        """Format results for display."""
        output = []
        output.append("\n" + "=" * 80)
        output.append("AI NEWS SUMMARY REPORT")
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 80)
        output.append("")
        
        for category, articles in results.items():
            if articles:
                output.append(f"\n{'=' * 80}")
                output.append(f"CATEGORY: {category.upper()}")
                output.append(f"{'=' * 80}\n")
                
                for i, article in enumerate(articles, 1):
                    output.append(f"\n[{i}] {article.get('title', 'No title')}")
                    output.append(f"    Source: {article.get('source', 'Unknown')}")
                    
                    if article.get('link'):
                        output.append(f"    Link: {article.get('link')}")
                    
                    if article.get('days_ago') is not None:
                        output.append(f"    Published: {article.get('days_ago')} days ago")
                    
                    # Show RSS summary if no AI summary available
                    if article.get('ai_summary'):
                        output.append(f"\n    AI Summary: {article.get('ai_summary')}")
                    elif article.get('summary'):
                        summary = article.get('summary', '')[:200]
                        if len(article.get('summary', '')) > 200:
                            summary += "..."
                        output.append(f"\n    Summary: {summary}")
                    
                    output.append("")
        
        return "\n".join(output)
    
    def save_results(self, results: Dict[str, List[Dict]], filename: str = None):
        """Save results to JSON file."""
        if filename is None:
            filename = f"ai_news_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Prepare data for JSON serialization
        json_data = {
            "generated_at": datetime.now().isoformat(),
            "categories": {}
        }
        
        for category, articles in results.items():
            json_data["categories"][category] = []
            for article in articles:
                json_article = {
                    "title": article.get("title"),
                    "source": article.get("source"),
                    "link": article.get("link"),
                    "published": article.get("published"),
                    "days_ago": article.get("days_ago"),
                    "ai_summary": article.get("ai_summary")
                }
                json_data["categories"][category].append(json_article)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {filename}")
