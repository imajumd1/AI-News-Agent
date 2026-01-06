"""Categorizes articles into AI Infrastructure and AI Frontier models."""

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
        
        matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        score = matches / len(keywords)
        
        # Boost score if multiple keywords found
        if matches > 1:
            score *= 1.2
        
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
        
        # Calculate scores for each category
        scores = {}
        for category in self.keywords.keys():
            scores[category] = self.calculate_category_score(full_text, category)
        
        # Find the category with the highest score
        best_category = max(scores.items(), key=lambda x: x[1])
        
        # Only categorize if score is above threshold
        if best_category[1] > 0.1:
            return best_category[0]
        
        return None
    
    def categorize_articles(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize multiple articles."""
        categorized = {
            "AI Infrastructure": [],
            "AI Frontier models": [],
            "AI Builder tools": [],
            "AI startups to watch": []
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
