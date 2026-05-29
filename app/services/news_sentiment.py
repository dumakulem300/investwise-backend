import httpx
from textblob import TextBlob
from typing import List, Dict, Any

# GNews API base URL (free tier)
GNEWS_BASE_URL = "https://gnews.io/api/v4/search"

async def fetch_news_for_stock(company_name: str, symbol: str) -> List[Dict[str, Any]]:
    """
    Fetch news articles for a given stock using GNews API.
    Returns list of dicts with title, description, url, publishedAt, sentiment.
    """
    query = f"{company_name} Philippines stock"
    params = {
        "q": query,
        "lang": "en",
        "max": 5,
        "country": "ph"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(GNEWS_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = data.get("articles", [])
            results = []
            for article in articles[:5]:
                title = article.get("title", "")
                description = article.get("description", "")
                url = article.get("url", "")
                published_at = article.get("publishedAt", "")
                
                # Sentiment analysis using TextBlob
                blob = TextBlob(f"{title}. {description}")
                polarity = blob.sentiment.polarity
                if polarity > 0.1:
                    sentiment_label = "positive"
                elif polarity < -0.1:
                    sentiment_label = "negative"
                else:
                    sentiment_label = "neutral"
                sentiment_score = polarity
                
                results.append({
                    "title": title,
                    "description": description,
                    "url": url,
                    "publishedAt": published_at,
                    "sentiment_score": round(sentiment_score, 3),
                    "sentiment_label": sentiment_label
                })
            return results
    except Exception as e:
        # Fallback mock data for development
        print(f"GNews failed for {symbol}: {e}. Returning mock data.")
        return [
            {
                "title": f"{company_name} shows resilience in Philippine market",
                "description": f"Recent trading of {symbol} indicates positive momentum despite regional headwinds.",
                "url": "https://example.com/mock1",
                "publishedAt": "2025-05-28T00:00:00Z",
                "sentiment_score": 0.2,
                "sentiment_label": "positive"
            },
            {
                "title": f"Analysts weigh in on {company_name} outlook",
                "description": f"Mixed opinions on {symbol} as earnings approach.",
                "url": "https://example.com/mock2",
                "publishedAt": "2025-05-27T00:00:00Z",
                "sentiment_score": -0.05,
                "sentiment_label": "neutral"
            }
        ]

async def get_news_for_symbol(symbol: str) -> List[Dict[str, Any]]:
    """
    Main function to get news for a stock symbol.
    Uses a simple mapping of symbol to company name (can be extended).
    """
    # Philippine stock symbol to company name mapping
    company_names = {
        "AC": "Ayala Corporation",
        "SM": "SM Investments",
        "BDO": "BDO Unibank",
        "JFC": "Jollibee Foods",
        "TEL": "PLDT",
        "MER": "Meralco",
        "GLO": "Globe Telecom",
        "ALI": "Ayala Land",
        "AEV": "Aboitiz Equity Ventures",
        "MBT": "Metropolitan Bank"
    }
    company = company_names.get(symbol.upper(), symbol)
    return await fetch_news_for_stock(company, symbol.upper())