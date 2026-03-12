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
            "GPU and AI Infra": [],
            "AI Applications": [],
            "AI Builder tools": [],
            "Cool Startups to watch": []
        }
        
        # Special handling for "Cool Startups to watch" category
        startups_category = "Cool Startups to watch"
        print(f"\nStep 4a: Fetching cool startups for '{startups_category}'...")
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
                    # Limit to top 10 most recent articles per category
                    top_articles = articles[:10]
                    print(f"\nProcessing {category} (top {len(top_articles)} of {len(articles)} articles)...")
                    
                    # Generate category-level summary first
                    category_summary = None
                    if hasattr(self.summarizer, 'generate_category_summary') and self.summarizer.client:
                        print(f"  Generating category overview...")
                        try:
                            category_summary = self.summarizer.generate_category_summary(top_articles, category)
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
                    # Only include articles that successfully get AI summaries
                    try:
                        summarized = self.summarizer.generate_summaries(top_articles, category)
                        # Filter to only articles with AI summaries
                        ai_summarized = [a for a in summarized if a.get('ai_summary')]
                        
                        if len(ai_summarized) < len(summarized):
                            print(f"  ℹ Filtered to {len(ai_summarized)} articles with AI summaries (removed {len(summarized) - len(ai_summarized)} without)")
                        
                        # Add category summary to results
                        for article in ai_summarized:
                            article["category_summary"] = category_summary
                        
                        results[category] = ai_summarized
                    except Exception as e:
                        print(f"  ✗ Summarization failed for category: {e}")
                        results[category] = []
                else:
                    results[category] = []
            
            # Handle Cool Startups category with intelligent filtering & scoring
            print(f"\nProcessing {startups_category}...")
            
            # Use specialized startup intelligence for "Cool Startups to watch"
            if startups_category == "Cool Startups to watch" and hasattr(self.summarizer, 'generate_startup_intelligence'):
                # Get articles categorized as startups
                startup_articles = categorized.get(startups_category, [])
                # Merge with any fetched startup items
                all_startup_content = startup_articles + startup_items
                
                if all_startup_content:
                    print(f"  Running 5-signal startup intelligence on {len(all_startup_content)} items...")
                    try:
                        startup_intelligence = self.summarizer.generate_startup_intelligence(all_startup_content)
                        if startup_intelligence:
                            print(f"  ✓ Startup intelligence generated (top 10 curated)")
                            # Limit to top 10 articles only
                            top_10_startups = all_startup_content[:10]
                            for item in top_10_startups:
                                item["category_summary"] = startup_intelligence
                            results[startups_category] = top_10_startups
                            print(f"  📊 Showing top 10 startups out of {len(all_startup_content)} candidates")
                        else:
                            print(f"  ⚠ Startup intelligence returned None, limiting to 10")
                            top_10 = all_startup_content[:10]
                            for item in top_10:
                                item["category_summary"] = startup_summary
                            results[startups_category] = top_10
                    except Exception as e:
                        print(f"  ⚠ Could not generate startup intelligence: {str(e)[:100]}")
                        top_10 = all_startup_content[:10]
                        for item in top_10:
                            item["category_summary"] = startup_summary
                        results[startups_category] = top_10
                    
                    # Always limit to 10
                    if len(results[startups_category]) > 10:
                        results[startups_category] = results[startups_category][:10]
                else:
                    results[startups_category] = []
            else:
                # Fallback to old method - limit to 10
                all_items = (categorized.get(startups_category, []) + startup_items)[:10]
                for startup in all_items:
                    startup["category_summary"] = startup_summary
                results[startups_category] = all_items
                print(f"  📊 Limited to top 10 startups (fallback mode)")
        else:
            # Without AI summaries enabled, return empty results
            # We don't show RSS summaries - only AI-curated content
            print("⚠ AI summaries are required. Fast mode is not supported.")
            print("  All categories will be empty without AI summarization enabled.")
            for category in results.keys():
                results[category] = []
        
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
                    
                    # Only show AI summaries - no RSS summaries
                    if article.get('ai_summary'):
                        output.append(f"\n    AI Summary: {article.get('ai_summary')}")
                    else:
                        output.append(f"\n    [No AI summary available]")
                    
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
