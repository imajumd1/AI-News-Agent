"""Categorizes articles into GPU and AI Infra, AI Applications, AI Builder tools, and Cool Startups."""

from typing import Dict, List, Optional
from config import CATEGORY_KEYWORDS


class ArticleCategorizer:
    """Categorizes articles based on content analysis."""
    
    def __init__(self):
        self.keywords = CATEGORY_KEYWORDS
    
    def calculate_category_score(self, text: str, category: str) -> float:
        """Calculate how well an article matches a category."""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        keywords = self.keywords.get(category, [])
        
        if not keywords:
            return 0.0
        
        # Count keyword matches (case-insensitive)
        matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        
        # Stricter scoring to ensure relevance
        # Require at least 2 keyword matches for good confidence
        if matches >= 2:
            # Base score of 0.4 for 2 matches, add 0.2 per additional match
            score = 0.4 + ((matches - 2) * 0.2)
        elif matches == 1:
            # Single match gets lower score (0.15) - only counts if no better category
            score = 0.15
        else:
            score = 0.0
        
        return min(score, 1.0)
    
    def categorize_article(self, article: Dict) -> Optional[str]:
        """Categorize a single article."""
        # Combine title, summary, and content for analysis
        text_parts = [
            article.get("title", ""),
            article.get("summary", ""),
            article.get("full_content", "")
        ]
        full_text = " ".join(text_parts)
        
        if not full_text.strip():
            return None
        
        # PRIORITY CHECK: "Cool Startups to watch" first to avoid being captured by generic "AI Applications"
        # Articles from Product Hunt, Show HN, Indie Hackers should go here even if they mention AI
        startup_score = self.calculate_category_score(full_text, "Cool Startups to watch")
        if startup_score > 0.3:  # Strong startup signal - assign immediately
            return "Cool Startups to watch"
        
        # Calculate scores for each category
        scores = {}
        for category in self.keywords.keys():
            scores[category] = self.calculate_category_score(full_text, category)
        
        # Find the category with the highest score
        best_category = max(scores.items(), key=lambda x: x[1])
        
        # Stricter threshold to ensure relevance - require at least 2 keyword matches
        # This translates to a score of at least 0.4
        threshold = 0.3
        
        # Only categorize if score is above threshold
        if best_category[1] > threshold:
            return best_category[0]
        
        return None
    
    def categorize_articles(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize multiple articles."""
        categorized = {
            "GPU and AI Infra": [],
            "AI Applications": [],
            "AI Builder tools": [],
            "Cool Startups to watch": []
        }
        
        uncategorized = []
        
        for article in articles:
            category = self.categorize_article(article)
            if category and category in categorized:
                article["category"] = category
                categorized[category].append(article)
            else:
                uncategorized.append(article)
        
        return categorized, uncategorized
