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
        "finance ai", "fintech ai", "ai finance", "ai banking", "ai trading",
        "education ai", "edtech ai", "ai education", "ai learning",
        "retail ai", "ai retail", "ai shopping", "ai commerce", "ai e-commerce",
        "manufacturing ai", "industrial ai", "ai manufacturing", "ai production",
        "transportation ai", "ai transportation", "autonomous", "self-driving",
        "agriculture ai", "agtech", "ai farming", "ai agriculture",
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
        "enterprise ai", "business ai", "ai business", "ai enterprise",
        "ai solution", "ai solutions", "ai platform", "ai platforms",
        "ai service", "ai services", "ai software", "ai tools", "ai tool",
        "ai product", "ai products", "ai feature", "ai features",
        "ai capability", "ai capabilities", "ai system", "ai systems",
        "ai integration", "ai workflow", "ai process", "ai processes",
        "ai company", "ai companies", "ai startup", "ai startups",
        
        # Consumer & Mobile Applications
        "ai app", "ai apps", "mobile ai", "ai mobile", "ai smartphone",
        "ai device", "ai devices", "smart device", "smart devices",
        "smart home", "ai home", "home ai", "iot ai", "ai iot",
        "ai wearable", "wearable ai", "ai gadget", "ai gadgets",
        
        # Popular AI Models & Services (when used in applications)
        "chatgpt", "gpt", "gpt-", "claude", "gemini", "bard",
        "copilot", "github copilot", "microsoft copilot",
        "ai agent", "ai agents", "intelligent agent", "smart agent",
        "openai", "anthropic", "google ai", "microsoft ai",
        
        # AI Technologies (application-focused)
        "computer vision", "image recognition", "face recognition", "object detection",
        "natural language", "nlp", "language model", "text generation",
        "neural network", "neural networks", "deep neural", "cnn", "rnn",
        "multimodal", "multimodal ai", "ai multimodal",
        "generative ai", "gen ai", "generative", "ai generation",
        
        # Application Context Terms
        "ai adoption", "adopting ai", "ai deployment", "deploying ai",
        "ai implementation", "implementing ai", "ai integration", "integrating ai",
        "ai pilot", "ai trial", "ai test", "testing ai",
        "ai project", "ai projects", "ai initiative", "ai program",
        "ai innovation", "ai breakthrough", "ai development", "developing ai",
        "ai research", "ai study", "ai study shows",
        
        # Real-World Application Phrases
        "how ai", "ai can", "ai will", "ai is", "ai has", "ai does",
        "ai to", "ai that", "ai which", "ai when", "ai where",
        "using ai", "with ai", "via ai", "through ai", "by ai",
        "ai helps", "ai enables", "ai allows", "ai makes",
        
        # Common Article Patterns
        "new ai", "latest ai", "ai news", "ai update", "ai announcement",
        "ai launch", "ai release", "ai unveils", "ai introduces",
        "ai partnership", "ai collaboration", "ai deal", "ai agreement"
    ],
    "AI Builder tools": [
        "developer tool", "sdk", "api", "framework", "library", "platform", "toolkit",
        "development", "programming", "code", "software", "build", "create", "tool",
        "ide", "editor", "assistant", "copilot", "autocomplete", "generation", "studio"
    ],
    "AI startups to watch": [
        "startup", "funding", "raise", "series a", "series b", "seed", "venture", "capital",
        "unicorn", "valuation", "ipo", "acquisition", "merger", "new company", "launch",
        "announcement", "backed", "investor", "accelerator", "incubator"
    ]
}

# Scraping Configuration
MAX_ARTICLES_PER_SOURCE = 2  # Reduced to 2 for faster scraping (54 sources)
REQUEST_TIMEOUT = 10  # Reduced timeout for faster failures
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
RATE_LIMIT_DELAY = 0.1  # Reduced delay between sources (0.1s instead of 0.3s for speed)