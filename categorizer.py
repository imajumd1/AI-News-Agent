"""Categorizes articles into GPU and AI Infra, AI Applications, AI Builder tools, and AI startups."""

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
        
        # For GPU and AI Infra and AI Applications, use a more lenient scoring
        if category == "GPU and AI Infra" or category == "AI Applications":
            # Very lenient - any match gets a good score
            if matches > 0:
                # Start at 0.2 for 1 match, add 0.15 per additional match
                # This ensures even single keyword matches get categorized
                score = 0.2 + (matches * 0.15)
            else:
                score = 0.0
        else:
            # Original scoring for other categories
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
        
        # Lower threshold for GPU and AI Infra and AI Applications categories to catch more articles
        # Very lenient threshold - any match above 0.01 is accepted
        threshold = 0.01 if best_category[0] in ["GPU and AI Infra", "AI Applications"] else 0.1
        
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
