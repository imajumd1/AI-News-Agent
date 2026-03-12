"""Configuration settings for the AI News Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Email Configuration
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)

# News Sources Configuration - Comprehensive AI News Coverage
NEWS_SOURCES = {
    # Tech Publications
    "techcrunch_ai": {
        "url": "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "type": "rss"
    },
    "crunchbase_news": {
        "url": "https://news.crunchbase.com/feed/",
        "type": "rss"
    },
    "the_verge_ai": {
        "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "type": "rss"
    },
    "wired_ai": {
        "url": "https://www.wired.com/feed/tag/artificial-intelligence/latest/rss",
        "type": "rss"
    },
    "mit_tech_review": {
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
        "type": "rss"
    },
    "venturebeat_ai": {
        "url": "https://venturebeat.com/ai/feed/",
        "type": "rss"
    },
    "zdnet_ai": {
        "url": "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
        "type": "rss"
    },
    "arstechnica_ai": {
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "type": "rss"
    },
    "engadget_ai": {
        "url": "https://www.engadget.com/rss.xml",
        "type": "rss"
    },
    
    # AI-Specific Blogs & Sites
    "hacker_news": {
        "url": "https://hnrss.org/newest?q=AI",
        "type": "rss"
    },
    "arxiv_ai": {
        "url": "http://arxiv.org/rss/cs.AI",
        "type": "rss"
    },
    "arxiv_ml": {
        "url": "http://arxiv.org/rss/cs.LG",
        "type": "rss"
    },
    "towards_data_science": {
        "url": "https://towardsdatascience.com/feed",
        "type": "rss"
    },
    "ai_news": {
        "url": "https://www.artificialintelligence-news.com/feed/",
        "type": "rss"
    },
    "synced_review": {
        "url": "https://syncedreview.com/feed/",
        "type": "rss"
    },
    "the_batch": {
        "url": "https://www.deeplearning.ai/the-batch/feed/",
        "type": "rss"
    },
    
    # Major Newspapers - Tech Sections
    "nytimes_tech": {
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "type": "rss"
    },
    "washington_post_tech": {
        "url": "https://feeds.washingtonpost.com/rss/business/technology",
        "type": "rss"
    },
    "guardian_tech": {
        "url": "https://www.theguardian.com/technology/artificialintelligenceai/rss",
        "type": "rss"
    },
    "bbc_tech": {
        "url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "type": "rss"
    },
    "reuters_tech": {
        "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
        "type": "rss"
    },
    
    # Industry & Business
    "bloomberg_tech": {
        "url": "https://www.bloomberg.com/feed/topics/technology",
        "type": "rss"
    },
    "wsj_tech": {
        "url": "https://feeds.a.dj.com/rss/RSSWSJD.xml",
        "type": "rss"
    },
    "forbes_ai": {
        "url": "https://www.forbes.com/innovation/feed2/",
        "type": "rss"
    },
    "cnbc_tech": {
        "url": "https://www.cnbc.com/id/19854910/device/rss/rss.html",
        "type": "rss"
    },
    
    # Research & Academic
    "nature_ai": {
        "url": "https://www.nature.com/subjects/artificial-intelligence.rss",
        "type": "rss"
    },
    "science_daily_ai": {
        "url": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
        "type": "rss"
    },
    "ieee_spectrum": {
        "url": "https://spectrum.ieee.org/rss/blog/artificial-intelligence/fulltext",
        "type": "rss"
    },
    
    # Developer & Technical
    "github_blog": {
        "url": "https://github.blog/feed/",
        "type": "rss"
    },
    "google_ai_blog": {
        "url": "https://ai.googleblog.com/feeds/posts/default",
        "type": "rss"
    },
    "openai_blog": {
        "url": "https://openai.com/blog/rss.xml",
        "type": "rss"
    },
    "anthropic_blog": {
        "url": "https://www.anthropic.com/index.xml",
        "type": "rss"
    },
    "aws_ml_blog": {
        "url": "https://aws.amazon.com/blogs/machine-learning/feed/",
        "type": "rss"
    },
    
    # GPU & Hardware Specific Sources
    "nvidia_blog": {
        "url": "https://blogs.nvidia.com/feed/",
        "type": "rss"
    },
    "tomshardware": {
        "url": "https://www.tomshardware.com/feeds/all",
        "type": "rss"
    },
    "anandtech": {
        "url": "https://www.anandtech.com/rss/",
        "type": "rss"
    },
    "techspot": {
        "url": "https://www.techspot.com/backend.xml",
        "type": "rss"
    },
    "the_information_tech": {
        "url": "https://www.theinformation.com/feed",
        "type": "rss"
    },
    
    # Business & AI Newsletters
    "axios_ai": {
        "url": "https://www.axios.com/feeds/axios-ai.rss",
        "type": "rss"
    },
    "axios_pro_rata": {
        "url": "https://www.axios.com/feeds/axios-pro-rata.rss",
        "type": "rss"
    },
    
    # AI Newsletters & Aggregators
    "ai_trends": {
        "url": "https://www.aitrends.com/feed/",
        "type": "rss"
    },
    "the_rundown_ai": {
        "url": "https://www.readtherundown.com/feed",
        "type": "rss"
    },
    "tldr_ai": {
        "url": "https://tldr.tech/ai/feed",
        "type": "rss"
    },
    "bens_bites": {
        "url": "https://www.bensbites.co/feed",
        "type": "rss"
    },
    "mindstream": {
        "url": "https://mindstream.ai/feed",
        "type": "rss"
    },
    
    # VC & Startup News
    "pitchbook": {
        "url": "https://pitchbook.com/news/rss",
        "type": "rss"
    },
    "vc_news_daily": {
        "url": "https://vcnewsdaily.com/feed/",
        "type": "rss"
    },
    "venture_capital_journal": {
        "url": "https://www.wsj.com/news/types/venture-capital?mod=rss_venture_capital",
        "type": "rss"
    },
    "strictly_vc": {
        "url": "https://strictlyvc.com/feed/",
        "type": "rss"
    },
    "a16z": {
        "url": "https://a16z.com/feed/",
        "type": "rss"
    },
    
    # Tech Publications - Regional
    "tech_in_asia": {
        "url": "https://www.techinasia.com/feed",
        "type": "rss"
    },
    "sifted": {
        "url": "https://sifted.eu/feed",
        "type": "rss"
    },
    "geekwire": {
        "url": "https://www.geekwire.com/feed/",
        "type": "rss"
    },
    
    # Additional Newsletters (if RSS available)
    "superhuman_newsletter": {
        "url": "https://superhuman.com/blog/rss",
        "type": "rss"
    },
    
    # Additional AI-Specific Sources
    "marktechpost": {
        "url": "https://www.marktechpost.com/feed/",
        "type": "rss"
    },
    "machine_learning_mastery": {
        "url": "https://machinelearningmastery.com/feed/",
        "type": "rss"
    },
    "papers_with_code": {
        "url": "https://paperswithcode.com/latest",
        "type": "rss"
    },
    "distill_pub": {
        "url": "https://distill.pub/rss.xml",
        "type": "rss"
    },
    
    # Developer & AI Tools Focus
    "hugging_face_blog": {
        "url": "https://huggingface.co/blog/feed.xml",
        "type": "rss"
    },
    "pytorch_blog": {
        "url": "https://pytorch.org/blog/feed.xml",
        "type": "rss"
    },
    "tensorflow_blog": {
        "url": "https://blog.tensorflow.org/feeds/posts/default",
        "type": "rss"
    },
    "databricks_blog": {
        "url": "https://www.databricks.com/blog/rss.xml",
        "type": "rss"
    },
    "weights_biases_blog": {
        "url": "https://wandb.ai/fully-connected/rss",
        "type": "rss"
    },
    
    # Tier 1 — Cool Startups to Watch (Best Signal, Free)
    "product_hunt": {
        "url": "https://www.producthunt.com/feed",
        "type": "rss"
    },
    "product_hunt_top": {
        "url": "https://www.producthunt.com/feed/today",
        "type": "rss"
    },
    "hacker_news_show": {
        "url": "https://hnrss.org/show",
        "type": "rss"
    },
    "yc_blog": {
        "url": "https://www.ycombinator.com/blog/feed",
        "type": "rss"
    },
    
    # Tier 2 — Cool Startups (Great Content)
    "techcrunch_startups": {
        "url": "https://techcrunch.com/tag/startups/feed/",
        "type": "rss"
    },
    "indie_hackers": {
        "url": "https://www.indiehackers.com/feed",
        "type": "rss"
    },
    
    # Tier 3 — Cool Startups (Niche but High Quality)
    "betalist": {
        "url": "https://betalist.com/feed",
        "type": "rss"
    },
    "wellfound": {
        "url": "https://wellfound.com/feed",
        "type": "rss"
    },
    "saastr": {
        "url": "https://www.saastr.com/feed/",
        "type": "rss"
    },
    "the_hustle": {
        "url": "https://thehustle.co/feed/",
        "type": "rss"
    },
    "techfundingnews": {
        "url": "https://techfundingnews.com/feed/",
        "type": "rss"
    },
    
    # International AI News
    "the_ai_report": {
        "url": "https://theaireport.com/feed/",
        "type": "rss"
    },
    "ai_business": {
        "url": "https://aibusiness.com/rss.xml",
        "type": "rss"
    },
    "ventureburn": {
        "url": "https://ventureburn.com/feed/",
        "type": "rss"
    },
    
    # More Tech Publications
    "fast_company_tech": {
        "url": "https://www.fastcompany.com/technology/rss",
        "type": "rss"
    },
    "hackernoon_ai": {
        "url": "https://hackernoon.com/tagged/ai/feed",
        "type": "rss"
    },
    "dev_to_ai": {
        "url": "https://dev.to/feed/tag/ai",
        "type": "rss"
    },
    "medium_ai": {
        "url": "https://medium.com/feed/tag/artificial-intelligence",
        "type": "rss"
    },
    
    # AI Ethics & Policy
    "ai_now": {
        "url": "https://ainowinstitute.org/feed",
        "type": "rss"
    },
    "future_of_life": {
        "url": "https://futureoflife.org/feed/",
        "type": "rss"
    },
    
    # Industry Analysis
    "cb_insights": {
        "url": "https://www.cbinsights.com/research/feed/",
        "type": "rss"
    },
    "protocol": {
        "url": "https://www.protocol.com/feed",
        "type": "rss"
    },
    
    # More Hardware & Infrastructure
    "serve_the_home": {
        "url": "https://www.servethehome.com/feed/",
        "type": "rss"
    },
    "data_center_knowledge": {
        "url": "https://www.datacenterknowledge.com/feed",
        "type": "rss"
    },
    
    # Additional Company Blogs
    "microsoft_ai_blog": {
        "url": "https://blogs.microsoft.com/ai/feed/",
        "type": "rss"
    },
    "meta_ai_blog": {
        "url": "https://ai.facebook.com/blog/rss/",
        "type": "rss"
    },
    "deepmind_blog": {
        "url": "https://deepmind.com/blog/feed/basic/",
        "type": "rss"
    },
    "cohere_blog": {
        "url": "https://cohere.com/blog/rss.xml",
        "type": "rss"
    },
    "stability_ai_blog": {
        "url": "https://stability.ai/blog/rss",
        "type": "rss"
    },
    "mistral_blog": {
        "url": "https://mistral.ai/news/rss/",
        "type": "rss"
    }
}

# Category Keywords
CATEGORY_KEYWORDS = {
    "GPU and AI Infra": [
        # Core AI Infrastructure
        "ai infrastructure", "ai stack", "ai platforms", "ml infrastructure",
        "machine learning platforms", "ai systems architecture", "ai compute infrastructure",
        "ai deployment infrastructure", "ai infrastructure stack", "mlops infrastructure",
        "ai operations", "ml operations", "ai platform", "ml platform",
        
        # GPU & Hardware - General
        "gpu", "gpus", "graphics processing unit", "graphics card", "video card",
        "gpu computing", "gpu acceleration", "gpu cluster", "gpu server", "gpu cloud",
        "gpu datacenter", "gpu infrastructure", "gpu training", "gpu inference",
        
        # NVIDIA Specific
        "nvidia", "nvidia cuda", "cuda", "cuda cores", "tensor cores", "tensorrt",
        "nvidia h100", "nvidia a100", "nvidia a800", "nvidia h800", "nvidia blackwell",
        "nvidia hopper", "nvidia ampere", "nvidia dgx", "nvidia superpod", "nvidia omniverse",
        "nvidia ai", "nvidia enterprise", "nvidia cloud", "nvidia datacenter",
        
        # AMD & Other GPU Vendors
        "amd", "amd gpu", "amd mi", "amd instinct", "amd rocm", "rocm",
        "intel gpu", "intel arc", "intel gaudi", "intel xeon",
        
        # AI Accelerators & Chips
        "ai accelerator", "ai accelerators", "ai chip", "ai chips", "ml accelerator",
        "neural processing unit", "npu", "tpu", "tensor processing unit", "tpu infrastructure",
        "google tpu", "cerebras", "graphcore", "samba nova", "groq", "mythic",
        "ai processor", "ml processor", "neural chip", "ai silicon",
        
        # Cloud & Datacenter Infrastructure
        "cloud ai", "ai cloud", "cloud gpu", "gpu cloud", "cloud infrastructure",
        "datacenter", "data center", "ai datacenter", "ml datacenter", "compute cluster",
        "training cluster", "inference cluster", "ai cluster", "ml cluster",
        "aws", "amazon web services", "aws sagemaker", "aws trainium", "aws inferentia",
        "google cloud", "gcp", "google cloud ai", "google cloud tpu", "google cloud gpu",
        "azure", "microsoft azure", "azure ml", "azure ai", "azure datacenter",
        "oracle cloud", "oracle ai", "ibm cloud", "ibm watson",
        
        # Edge & Mobile AI Hardware
        "edge ai", "edge computing", "edge ai hardware", "mobile ai", "on-device ai",
        "embedded ai", "iot ai", "edge inference", "edge training",
        
        # Heterogeneous Computing & Specialized Hardware
        "heterogeneous computing", "specialized hardware", "custom silicon", "custom chip",
        "ai asic", "ml asic", "domain-specific architecture", "dsa",
        
        # Infrastructure & Deployment Tools
        "kubernetes", "k8s", "docker", "container", "orchestration", "deployment",
        "scaling", "distributed training", "distributed inference", "model serving",
        "model deployment", "inference serving", "ml pipeline", "data pipeline",
        "storage", "networking", "optimization", "efficiency", "performance",
        
        # Frameworks & Software Infrastructure
        "tensorflow", "pytorch", "jax", "triton", "tensorrt", "onnx", "openvino",
        "ml framework", "deep learning framework", "ai framework",
        
        # Physical AI & Infrastructure
        "physical ai", "ai hardware", "ml hardware", "compute hardware",
        "training infrastructure", "inference infrastructure", "serving infrastructure",
        
        # Companies & Products
        "openai infrastructure", "anthropic infrastructure", "cohere infrastructure",
        "databricks", "snowflake", "hugging face", "huggingface", "weights & biases",
        "wandb", "mlflow", "kubeflow", "ray", "dask",
        
        # General Infrastructure Terms
        "infrastructure", "compute", "hardware", "chips", "processors", "servers",
        "scaling", "capacity", "throughput", "latency", "bandwidth"
    ],
    "AI Applications": [
        # Core AI Application Terms (most common in headlines)
        "ai", "artificial intelligence", "machine learning", "ml", "deep learning",
        "ai-powered", "ai-driven", "powered by ai", "using ai", "with ai",
        "ai application", "ai applications", "ai use", "ai uses", "ai usage",
        
        # Common Application Verbs & Actions
        "ai helps", "ai enables", "ai improves", "ai enhances", "ai transforms",
        "ai revolutionizes", "ai changes", "ai automates", "ai assists",
        "ai analyzes", "ai predicts", "ai detects", "ai recognizes", "ai generates",
        "ai creates", "ai writes", "ai designs", "ai develops", "ai builds",
        
        # Industry & Sector Applications (broad terms)
        "ai in", "ai for", "ai and", "ai +", "ai meets",
        "healthcare ai", "medical ai", "ai healthcare", "ai medicine",
        "ai finance", "ai banking", "ai trading",
        "ai education", "ai learning",
        "retail ai", "ai retail", "ai shopping", "ai commerce", "ai e-commerce",
        "manufacturing ai", "industrial ai", "ai manufacturing", "ai production",
        "transportation ai", "ai transportation", "autonomous", "self-driving",
        "ai farming", "ai agriculture",
        "energy ai", "ai energy", "ai utilities",
        
        # Application Types (common in articles)
        "chatbot", "chatbots", "ai chatbot", "ai chat", "conversational ai",
        "virtual assistant", "ai assistant", "digital assistant", "smart assistant",
        "ai recommendation", "recommendation system", "ai suggestions",
        "ai personalization", "personalized ai", "ai customization",
        "ai content", "content generation", "ai generation", "ai generated",
        "ai image", "image generation", "ai photo", "ai picture", "ai visual",
        "ai video", "video generation", "ai film", "ai animation",
        "ai music", "ai audio", "ai sound", "ai voice", "voice ai",
        "ai art", "ai artist", "ai creative", "ai creativity",
        "ai translation", "ai language", "language ai", "ai speech", "speech ai",
        "ai search", "ai discovery", "ai find", "ai explore",
        "ai analytics", "ai analysis", "ai insights", "ai intelligence",
        "ai prediction", "ai forecast", "ai forecasting", "ai predict",
        "ai optimization", "ai optimize", "ai efficiency",
        "ai automation", "automated ai", "ai automatic",
        "ai decision", "decision making", "ai choices",
        
        # Enterprise & Business Applications
        "enterprise ai", "ai enterprise",
        "ai system", "ai systems",
        "ai workflow", "ai process", "ai processes",
        
        # Consumer & Mobile Applications
        "mobile ai", "ai mobile", "ai smartphone",
        "ai device", "ai devices", "smart device", "smart devices",
        "smart home", "ai home", "home ai", "iot ai", "ai iot",
        "ai wearable", "wearable ai", "ai gadget", "ai gadgets",
        
        # Popular AI Models & Services (when used in end-user applications)
        "chatgpt", "gpt-4", "claude", "gemini", "bard",
        "microsoft copilot", "windows copilot",
        
        # AI Technologies (application-focused)
        "computer vision", "image recognition", "face recognition", "object detection",
        "natural language", "nlp", "language model", "text generation",
        "neural network", "neural networks", "deep neural", "cnn", "rnn",
        "multimodal", "multimodal ai", "ai multimodal",
        "generative ai", "gen ai", "generative", "ai generation",
        
        # Application Context Terms (end-user focused)
        "ai adoption", "adopting ai",
        "ai pilot", "ai trial",
        "ai innovation", "ai breakthrough",
        "ai research", "ai study", "ai study shows",
        
        # Application-Specific Phrases (more selective)
        "ai application", "ai use case",
        "ai powered", "powered by ai", "ai-powered"
    ],
    "AI Builder tools": [
        # AI Development Frameworks & Tools
        "langchain", "llamaindex", "llama index", "hugging face", "huggingface", "transformers",
        "pytorch", "tensorflow", "keras", "onnx", "mlflow", "wandb", "weights & biases", 
        "gradio", "streamlit", "fastapi", "flask ai",
        
        # AI Code Assistants & IDEs  
        "github copilot", "copilot", "cursor", "replit", "codeium", "tabnine", "codex", 
        "code assistant", "ai coding", "code generation", "pair programming", "ai code",
        "coding assistant", "code completion",
        
        # Vector DBs & RAG Tools
        "pinecone", "weaviate", "qdrant", "chroma", "chromadb", "milvus", "vector database", 
        "vector db", "embeddings", "embedding", "rag", "retrieval augmented", "semantic search",
        "vector store", "vector search",
        
        # AI Development Platforms & APIs
        "openai api", "gpt api", "anthropic api", "claude api", "cohere", "replicate", 
        "modal", "beam", "together ai", "fireworks ai", "anyscale", "baseten", 
        "inference api", "ai api", "llm api", "api key", "api integration",
        
        # Model Training & Fine-tuning
        "fine-tuning", "fine tuning", "finetune", "model training", "train model",
        "model optimization", "lora", "qlora", "peft", "parameter efficient", 
        "model deployment", "deploy model", "model serving", "serve model",
        
        # AI Agent Frameworks
        "autogpt", "babyagi", "agent framework", "langflow", "flowise", 
        "autonomous agent", "ai agent", "tool calling", "function calling",
        "langchain agent", "agent toolkit",
        
        # Prompt Engineering & Testing
        "prompt engineering", "prompt", "prompting", "prompt playground", "langsmith", 
        "helicone", "promptfoo", "ai testing", "llm evaluation", "prompt optimization",
        "prompt template", "few shot",
        
        # Development Terms
        "ai sdk", "sdk", "developer", "developer tool", "development", "build with ai",
        "ai framework", "framework", "library", "package", "tool", "toolkit",
        "machine learning tool", "ml tool", "ml platform", "mlops",
        "ai builder", "no-code ai", "low-code ai", "ai development",
        
        # Common Dev Patterns
        "integration", "integrate", "build", "create", "develop", "implementation",
        "tutorial", "guide", "documentation", "docs", "api reference",
        "getting started", "quickstart", "example", "sample code"
    ],
    "Cool Startups to watch": [
        # Funding & Investment (high weight)
        "startup", "startups", "founded", "founder", "founders", "co-founder", "cofounder", "founding team",
        "funding", "raise", "raised", "raises", "raising", 
        "series a", "series b", "series c", "series d", "seed round", "seed funding", "pre-seed",
        "venture", "capital", "vc", "venture capital", "venture-backed",
        "investment", "invested", "investor", "investors", "angel", "angel investor",
        "unicorn", "decacorn", "valuation", "valued at", "worth",
        "ipo", "going public", "public offering",
        "acquisition", "acquired", "acquires", "buying", "bought by",
        "merger", "merging", "exit", "exits",
        "million", "billion", "m in", "b in", "$",
        
        # Company Stage & Activity
        "new company", "new startup", "launches", "launched", "launching", "unveils", "debuts",
        "stealth", "stealth mode", "coming out of stealth", "emerges from stealth",
        "announcement", "announces", "unveiled", "introduced", "introducing",
        "backed", "backed by", "led by", "investors include",
        "accelerator", "incubator", "yc", "y combinator", "ycombinator",
        "techstars", "500 startups", "demo day",
        
        # Product & Growth (very startup-specific)
        "product hunt", "producthunt", "show hn", "show hackernews",
        "indie hacker", "indie hackers", "indiehackers",
        "bootstrapped", "self-funded", "profitable", "break even",
        "built by", "created by", "made by", "founded by",
        "side project", "weekend project", "solo founder", "one person", "small team",
        "revenue", "arr", "mrr", "monthly recurring", "annual recurring",
        "growth", "growing", "traction", "scale", "scaling", "scaled",
        "users", "customers", "subscribers", "downloads", "installs", "signups",
        "waitlist", "beta", "alpha", "early access", "pre-launch", "coming soon",
        
        # Startup Types & Tech
        "saas", "b2b", "b2c", "b2b2c", "d2c",
        "marketplace", "two-sided marketplace", "platform",
        "productivity", "productivity tool", "automation", "automate",
        "workflow", "collaboration", "collaboration tool",
        "no-code", "nocode", "low-code", "lowcode",
        "fintech", "edtech", "healthtech", "proptech", "insurtech",
        "cleantech", "climatetech", "greentech",
        "crypto", "cryptocurrency", "web3", "blockchain", "nft", "defi", "dao",
        
        # Founder Journey & Community
        "building", "building in public", "shipping", "launched today", "just launched",
        "we built", "we're building", "we made", "we created",
        "indie", "solo", "maker", "makers", "hacker", "builder", "builders",
        "entrepreneur", "entrepreneurship", "solopreneur",
        "remote team", "distributed team", "remote-first",
        
        # Business model & monetization
        "freemium", "pricing", "subscription", "monthly plan", "annual plan",
        "business model", "revenue model", "monetization", "monetize",
        "paying customers", "revenue growth",
        
        # Startup ecosystem terms
        "pitch", "pitching", "pitch deck", "demo",
        "pivot", "pivoting", "pivoted",
        "mvp", "minimum viable product", "prototype",
        "early stage", "growth stage", "late stage"
    ]
}

# Scraping Configuration
MAX_ARTICLES_PER_SOURCE = 2  # Reduced to 2 for faster scraping (54 sources)
REQUEST_TIMEOUT = 10  # Reduced timeout for faster failures
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
RATE_LIMIT_DELAY = 0.1  # Reduced delay between sources (0.1s instead of 0.3s for speed)