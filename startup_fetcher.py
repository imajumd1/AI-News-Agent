"""Fetches top AI enterprise startups and generates summaries."""

from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from config import USER_AGENT, REQUEST_TIMEOUT
from summarizer import ArticleSummarizer
import time


class StartupFetcher:
    """Fetches top AI enterprise startups."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.summarizer = ArticleSummarizer()
    
    def get_top_ai_enterprise_startups(self) -> List[Dict]:
        """
        Returns a curated list of top 10 AI enterprise startups.
        This is a curated list based on market research and industry recognition.
        """
        startups = [
            {
                "name": "Anthropic",
                "website": "https://www.anthropic.com",
                "description": "AI safety company building Claude, a next-generation AI assistant focused on helpfulness, harmlessness, and honesty.",
                "focus": "AI Safety & Enterprise AI Assistants"
            },
            {
                "name": "Cohere",
                "website": "https://cohere.com",
                "description": "Enterprise AI platform providing large language models and NLP APIs for businesses.",
                "focus": "Enterprise LLM APIs & NLP"
            },
            {
                "name": "Adept AI",
                "website": "https://www.adept.ai",
                "description": "Building AI systems that can use software tools and APIs to accomplish complex tasks.",
                "focus": "AI Agents & Automation"
            },
            {
                "name": "Scale AI",
                "website": "https://scale.com",
                "description": "Data platform for AI providing high-quality training data and model evaluation for enterprise AI.",
                "focus": "AI Data Infrastructure & Training"
            },
            {
                "name": "Hugging Face",
                "website": "https://huggingface.co",
                "description": "Open-source AI platform providing models, datasets, and tools for the AI community and enterprises.",
                "focus": "Open-Source AI Platform & Model Hub"
            },
            {
                "name": "Weights & Biases",
                "website": "https://wandb.ai",
                "description": "MLOps platform for experiment tracking, model management, and collaboration for ML teams.",
                "focus": "MLOps & Experiment Tracking"
            },
            {
                "name": "Runway",
                "website": "https://runwayml.com",
                "description": "Creative AI tools for content generation, video editing, and multimedia creation for enterprises.",
                "focus": "Creative AI & Content Generation"
            },
            {
                "name": "Jasper AI",
                "website": "https://www.jasper.ai",
                "description": "AI content platform for marketing teams to generate copy, blog posts, and marketing materials.",
                "focus": "AI Content Generation for Marketing"
            },
            {
                "name": "C3.ai",
                "website": "https://c3.ai",
                "description": "Enterprise AI software platform for accelerating digital transformation across industries.",
                "focus": "Enterprise AI Applications"
            },
            {
                "name": "DataRobot",
                "website": "https://www.datarobot.com",
                "description": "Automated machine learning platform that enables organizations to build and deploy AI models faster.",
                "focus": "AutoML & Model Deployment"
            }
        ]
        
        return startups
    
    def enrich_startup_info(self, startup: Dict) -> Dict:
        """Enrich startup information with additional details."""
        # Try to fetch more info from the website if needed
        # For now, we'll use the curated data
        return {
            "title": startup["name"],
            "link": startup["website"],
            "source": "AI Enterprise Startups",
            "description": startup["description"],
            "focus": startup["focus"],
            "published": None,
            "days_ago": None,
            "summary": startup["description"]
        }
    
    def generate_startups_summary(self, startups: List[Dict]) -> Optional[str]:
        """Generate an AI summary of the top AI enterprise startups."""
        if not self.summarizer.client:
            return None
        
        # Prepare startup information for summary
        startup_info = []
        for i, startup in enumerate(startups[:10], 1):
            info = f"{i}. {startup['name']} ({startup['website']}): {startup['description']} Focus: {startup['focus']}"
            startup_info.append(info)
        
        startups_text = "\n".join(startup_info)
        
        prompt = f"""You are an AI industry analyst. Analyze the following top 10 AI enterprise startups and create a comprehensive summary (5-7 sentences) that covers:

1. The overall landscape and trends in AI enterprise startups
2. Key focus areas and market segments these startups are targeting
3. Notable innovations or differentiators
4. The direction of enterprise AI adoption
5. What makes these companies stand out in the market

Top AI Enterprise Startups:
{startups_text}

Provide an insightful, cohesive summary that gives readers a comprehensive understanding of the current state of AI enterprise startups:"""
        
        try:
            response = self.summarizer.client.chat.completions.create(
                model=self.summarizer.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI industry analyst. Create comprehensive, insightful summaries about AI enterprise startups that synthesize information into a cohesive narrative."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating startups summary: {e}")
            return None
    
    def fetch_startups(self) -> tuple[List[Dict], Optional[str]]:
        """Fetch top AI enterprise startups and generate summary."""
        print("  Fetching top 10 AI enterprise startups...")
        
        # Get curated list of startups
        startups = self.get_top_ai_enterprise_startups()
        
        # Enrich startup information
        enriched_startups = [self.enrich_startup_info(startup) for startup in startups]
        
        print(f"  Found {len(enriched_startups)} startups")
        
        # Generate AI summary
        category_summary = None
        if self.summarizer.client:
            print("  Generating AI summary of startups...")
            category_summary = self.generate_startups_summary(startups)
            if category_summary:
                print(f"  ✓ Summary generated ({len(category_summary)} chars)")
            else:
                print("  ⚠ Summary generation failed")
        else:
            print("  ⚠ Skipping summary - OpenAI API key not configured")
        
        return enriched_startups, category_summary
