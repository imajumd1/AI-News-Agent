"""Generates summaries of articles using LLM."""

from typing import List, Dict, Optional
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
from datetime import datetime


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
        
        # Adjust tone based on category
        if category == "Cool Startups to watch":
            system_prompt = "You are a warm, friendly tech writer speaking to college students who love startups. Write in an engaging, conversational tone that gets them excited about new companies and products."
            user_prompt = f"""Check out this cool startup/product! Write a friendly, engaging summary (2-3 sentences) that would excite a techy college student.

Title: {title}

Content:
{text}

Write a warm, conversational summary that highlights what makes this startup cool or interesting:"""
        else:
            system_prompt = "You are a concise AI news analyst. Generate brief, informative summaries."
            user_prompt = f"""You are an AI news analyst. Generate a concise, informative summary (2-3 sentences) of the following article about {category}.

Title: {title}

Content:
{text}

Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None
    
    def generate_summaries(self, articles: List[Dict], category: str, max_workers: int = 5) -> List[Dict]:
        """Generate summaries for multiple articles in parallel for faster processing."""
        if not articles:
            return []
        
        summarized_articles = []
        
        # Use ThreadPoolExecutor for parallel API calls
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all summary generation jobs
            future_to_article = {
                executor.submit(self.generate_summary, article, category): article
                for article in articles
            }
            
            completed = 0
            total = len(articles)
            
            # Process results as they complete
            for future in as_completed(future_to_article):
                article = future_to_article[future]
                completed += 1
                
                try:
                    summary = future.result(timeout=30)
                    if summary:
                        article["ai_summary"] = summary
                        print(f"  [{completed}/{total}] ✓ {article['title'][:50]}")
                    else:
                        print(f"  [{completed}/{total}] ⚠ No summary: {article['title'][:50]}")
                    summarized_articles.append(article)
                except Exception as e:
                    print(f"  [{completed}/{total}] ✗ Error: {article['title'][:50]} - {str(e)[:50]}")
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
        
        # Adjust tone based on category
        if category == "Cool Startups to watch":
            system_prompt = "You are a warm, enthusiastic tech writer who gets college students excited about startups. Write in a friendly, conversational tone that makes them want to explore these companies."
            user_prompt = f"""Hey! Check out these cool startups and products that launched recently. Write a warm, engaging overview (2-3 sentences) that would get a techy college student excited:

{articles_text}

Write a friendly summary that captures what's cool and interesting about these startups:"""
        else:
            system_prompt = "You are an expert AI news analyst. Create succinct, professional category-level summaries that are concise yet informative. Write in a clear, journalistic style."
            user_prompt = f"""You are an AI news analyst. Analyze the following articles about {category} and create a succinct, professional summary (2-3 sentences) that captures:

1. The main themes and trends
2. Key developments and breakthroughs
3. Important implications or impacts

Articles:
{articles_text}

Provide a concise, professional summary that gives readers a clear understanding of what's happening in {category} based on these articles. Be direct and informative:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=250,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating category summary: {e}")
            return None
    
    def generate_startup_intelligence(self, articles: List[Dict]) -> Optional[str]:
        """Generate curated startup summary with 5-signal scoring for college students."""
        if not self.client or not articles:
            return None
        
        # Collect article information
        article_info = []
        for i, article in enumerate(articles[:30], 1):  # Use more articles for better filtering
            title = article.get("title", "")
            summary = article.get("summary", "")
            link = article.get("link", "")
            source = article.get("source", "")
            article_info.append(f"{i}. [{title}]({link}) | Source: {source}\n   Summary: {summary[:400]}")
        
        articles_text = "\n\n".join(article_info)
        today = datetime.now().strftime("%B %d, %Y")
        
        system_prompt = """You are a startup intelligence analyst writing for a smart college-age audience (18-24) who are curious about technology, careers, and entrepreneurship but have limited time.

You will receive a list of raw startup articles, Product Hunt launches, and Hacker News posts from the past 7 days.

Your job:

STEP 1 — FILTER
Remove anything that is:
- An established company (> 5 years old or > 100 employees)
- A funding announcement with no product yet live
- A rebrand or pivot of an existing company
- Vague ("AI platform for enterprises") with no specific use case
- Pure crypto / NFT / Web3

STEP 2 — SCORE each startup on these 5 signals (1-10 each):
1. NOVELTY: Is this genuinely new or a copy of something existing?
2. TIMING: Does it solve a problem that is urgent right now in 2025?
3. FOUNDER SIGNAL: Solo founder, ex-FAANG, repeat founder, YC — any of these add points
4. TRACTION PROOF: User numbers, revenue, waitlist, upvotes, HN points
5. COLLEGE RELEVANCE: Would a 20-year-old student find this immediately useful or exciting?

STEP 3 — SELECT the top 10 by total score

STEP 4 — For each of the top 10, write a summary in exactly this format:

🚀 [STARTUP NAME]
One-line pitch: [What it does in plain English, no jargon]
Why now: [Why this exists in 2025 specifically]
Why you should care: [Hook for a college student — career, money, curiosity, or utility angle]
Traction: [Any numbers — users, revenue, upvotes, funding] OR "traction unknown" if missing
Built by: [Founder background if known, otherwise skip this line]
Link: [URL]

TONE: Curious, energetic, smart but never condescending. Think "smart friend who follows startups" not "press release."
NEVER use the words: "innovative", "disruptive", "revolutionary", "game-changing", "leverage", "synergy"
LENGTH: Each summary max 4 lines (excluding Built by line). No exceptions.

CRITICAL: If traction data is missing, say "traction unknown" — do not infer or guess. A startup with unknown traction but high novelty and timing scores can still make the top 10."""
        
        user_prompt = f"""Search the following sources for startups launched or funded in the last 7 days:

Articles:
{articles_text}

Today's date: {today}

Prioritise startups that:
- Have at least one of: live product, paying users, public waitlist, or disclosed funding under $10M
- Are in these spaces: AI tools, developer productivity, health tech, edtech, climate, consumer apps, creator economy
- Were founded 2023 or later

Deprioritise: enterprise-only B2B with no consumer angle, hardware without software, pure consulting firms

Run the 5-signal scoring. Return top 10 only in the exact format specified."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating startup intelligence: {e}")
            return None