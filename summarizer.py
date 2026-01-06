"""Generates summaries of articles using LLM."""

from typing import List, Dict, Optional
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL


class ArticleSummarizer:
    """Generates concise summaries of articles using LLM."""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            self.client = None
            self.model = None
            print("Warning: OPENAI_API_KEY not set. Summarization will be skipped.")
        else:
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL
            )
            self.model = OPENAI_MODEL
    
    def generate_summary(self, article: Dict, category: str) -> Optional[str]:
        """Generate a summary for a single article."""
        if not self.client:
            return None
        
        title = article.get("title", "")
        summary = article.get("summary", "")
        content = article.get("full_content", "")
        
        # Combine available text
        text = content if content else summary
        if not text:
            text = title
        
        # Truncate if too long
        if len(text) > 4000:
            text = text[:4000] + "..."
        
        prompt = f"""You are an AI news analyst. Generate a concise, informative summary (2-3 sentences) of the following article about {category}.

Title: {title}

Content:
{text}

Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a concise AI news analyst. Generate brief, informative summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None
    
    def generate_summaries(self, articles: List[Dict], category: str) -> List[Dict]:
        """Generate summaries for multiple articles."""
        summarized_articles = []
        
        for article in articles:
            print(f"  Summarizing: {article['title'][:50]}...")
            summary = self.generate_summary(article, category)
            if summary:
                article["ai_summary"] = summary
                summarized_articles.append(article)
        
        return summarized_articles
    
    def generate_category_summary(self, articles: List[Dict], category: str) -> Optional[str]:
        """Generate an overall summary for a category based on all articles."""
        if not self.client or not articles:
            return None
        
        # Collect article information
        article_info = []
        for i, article in enumerate(articles[:10], 1):  # Limit to 10 articles for context
            title = article.get("title", "")
            summary = article.get("summary", "") or article.get("ai_summary", "")
            if summary:
                article_info.append(f"{i}. {title}: {summary[:300]}")
            else:
                article_info.append(f"{i}. {title}")
        
        articles_text = "\n".join(article_info)
        
        prompt = f"""You are an AI news analyst. Analyze the following articles about {category} and create a comprehensive bird's-eye view summary (4-6 sentences) that captures:

1. The main themes and trends
2. Key developments and breakthroughs
3. Important implications or impacts
4. Overall direction of the field

Articles:
{articles_text}

Provide a cohesive summary that gives readers a comprehensive understanding of what's happening in {category} based on these articles:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI news analyst. Create comprehensive, insightful category-level summaries that synthesize multiple articles into a cohesive narrative."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating category summary: {e}")
            return None