"""
Saudi Market News Service
Fetches live business news from Saudi RSS feeds.
"""
import feedparser
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import re
import hashlib


@dataclass
class NewsItem:
    title: str
    source: str
    date: str
    summary: str
    url: str
    category: str = "General"
    sentiment: str = "Neutral"
    
    @property
    def id(self) -> str:
        return hashlib.md5(self.url.encode()).hexdigest()[:8]


# RSS Feed sources for Saudi business news
RSS_FEEDS = {
    "Arab News": "https://www.arabnews.com/taxonomy/term/466/feed",
    "Saudi Gazette": "https://saudigazette.com.sa/rss",
    "Gulf Business": "https://gulfbusiness.com/feed/",
    "MENAFN": "https://menafn.com/rss/menafn_sa.xml",
}

# Keywords for auto-categorization
CATEGORY_KEYWORDS = {
    "Construction": ["construction", "build", "infrastructure", "contractor", "cement", "steel", "real estate", "housing"],
    "Energy": ["oil", "gas", "aramco", "energy", "solar", "renewable", "hydrogen", "petroleum", "refinery"],
    "Technology": ["tech", "digital", "ai", "artificial intelligence", "cyber", "software", "cloud", "data", "fintech", "smart"],
    "Tourism": ["tourism", "hotel", "hospitality", "resort", "entertainment", "travel", "visitor", "red sea"],
    "Healthcare": ["health", "hospital", "medical", "pharma", "biotech", "clinic", "healthcare"],
    "Finance": ["bank", "investment", "fund", "ipo", "stock", "tadawul", "financial", "sukuk", "bond"],
    "Defense": ["defense", "military", "security", "gami", "sami", "aerospace"],
    "Transport": ["transport", "aviation", "airline", "railway", "port", "logistics", "shipping"],
    "Mega Projects": ["neom", "the line", "oxagon", "trojena", "qiddiya", "diriyah", "roshn", "kafd", "jeddah tower"],
}

POSITIVE_KEYWORDS = ["growth", "increase", "expand", "launch", "award", "win", "record", "boost", "surge", "billion", "partnership", "opportunity"]
NEGATIVE_KEYWORDS = ["decline", "loss", "delay", "cancel", "suspend", "cut", "risk", "crisis", "downturn", "shortage"]


def categorize_article(text: str) -> str:
    """Auto-categorize article based on keyword matching."""
    text_lower = text.lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[category] = score
    if scores:
        return max(scores, key=scores.get)
    return "General"


def get_sentiment(text: str) -> str:
    """Simple keyword-based sentiment analysis."""
    text_lower = text.lower()
    pos = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    neg = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)
    if pos > neg:
        return "Positive"
    elif neg > pos:
        return "Negative"
    return "Neutral"


def clean_html(raw_html: str) -> str:
    """Remove HTML tags from text."""
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', '', raw_html)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:500]  # Limit summary length


def fetch_news(max_per_source: int = 15) -> List[NewsItem]:
    """Fetch news from all configured RSS feeds."""
    all_news = []
    
    for source_name, feed_url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:max_per_source]:
                title = entry.get("title", "No Title")
                summary = clean_html(entry.get("summary", entry.get("description", "")))
                link = entry.get("link", "")
                
                # Parse date
                published = entry.get("published", entry.get("updated", ""))
                try:
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        dt = datetime(*entry.published_parsed[:6])
                        date_str = dt.strftime("%Y-%m-%d %H:%M")
                    else:
                        date_str = published[:16] if published else "Unknown"
                except Exception:
                    date_str = "Unknown"
                
                combined_text = f"{title} {summary}"
                category = categorize_article(combined_text)
                sentiment = get_sentiment(combined_text)
                
                all_news.append(NewsItem(
                    title=title,
                    source=source_name,
                    date=date_str,
                    summary=summary,
                    url=link,
                    category=category,
                    sentiment=sentiment,
                ))
        except Exception as e:
            # Silently skip failed feeds
            all_news.append(NewsItem(
                title=f"⚠️ Could not load feed: {source_name}",
                source=source_name,
                date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                summary=f"Feed temporarily unavailable. Error: {str(e)[:100]}",
                url="",
                category="System",
                sentiment="Neutral",
            ))
    
    # Sort by date descending
    all_news.sort(key=lambda x: x.date, reverse=True)
    return all_news


def get_news_summary(news_items: List[NewsItem]) -> dict:
    """Generate summary statistics from news items."""
    categories = {}
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    sources = {}
    
    for item in news_items:
        if item.category != "System":
            categories[item.category] = categories.get(item.category, 0) + 1
            sentiments[item.sentiment] = sentiments.get(item.sentiment, 0) + 1
            sources[item.source] = sources.get(item.source, 0) + 1
    
    return {
        "total": len([i for i in news_items if i.category != "System"]),
        "categories": categories,
        "sentiments": sentiments,
        "sources": sources,
    }
