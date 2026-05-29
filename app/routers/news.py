from fastapi import APIRouter, HTTPException
from app.services.news_sentiment import get_news_for_symbol
from app.services.stock_service import PH_BLUE_CHIPS

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/{symbol}")
async def get_stock_news(symbol: str):
    """Get latest news and sentiment for a specific stock symbol"""
    symbol = symbol.upper()
    if symbol not in PH_BLUE_CHIPS:
        raise HTTPException(status_code=404, detail="Symbol not in Philippine blue chips list")
    
    news = await get_news_for_symbol(symbol)
    if not news:
        raise HTTPException(status_code=503, detail="News service unavailable")
    
    return {"symbol": symbol, "articles": news}

@router.get("/all")
async def get_all_news():
    """Aggregated news for all blue chip stocks (first article per stock)"""
    all_news = []
    for symbol in PH_BLUE_CHIPS:
        news = await get_news_for_symbol(symbol)
        if news:
            all_news.append({
                "symbol": symbol,
                "top_article": news[0] if news else None
            })
    return {"stocks": all_news}