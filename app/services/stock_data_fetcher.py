import requests
import logging
from datetime import datetime, timedelta
from time import sleep
from app.database import db
from app.models import PREDICTIONS_COLLECTION
from app.config import settings

logger = logging.getLogger(__name__)

BLUE_CHIPS = ["AC", "SM", "BDO", "JFC", "TEL", "MER", "GLO", "ALI", "AEV", "MBT"]
EXCHANGE = "XPHS"  # PSE exchange code for Twelve Data

def fetch_from_twelvedata(symbol: str) -> dict:
    """Fetch latest daily price from Twelve Data API."""
    api_key = settings.TWELVEDATA_API_KEY
    if not api_key:
        logger.error("TWELVEDATA_API_KEY not set. Cannot fetch prices.")
        return None
    ticker = f"{symbol}:{EXCHANGE}"
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": ticker,
        "interval": "1day",
        "outputsize": 1,
        "apikey": api_key
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if "values" in data and len(data["values"]) > 0:
                latest = data["values"][0]
                close = float(latest["close"])
                date = latest["datetime"]
                volume = int(latest.get("volume", 0))
                return {"price": close, "date": date, "volume": volume}
            else:
                logger.warning(f"Twelve Data no values for {symbol}: {data}")
        else:
            logger.error(f"Twelve Data HTTP {resp.status_code} for {symbol}: {resp.text}")
    except Exception as e:
        logger.error(f"Twelve Data request failed for {symbol}: {e}")
    return None

def update_predictions():
    """Fetch latest prices for all blue chips and store in Firestore."""
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    for symbol in BLUE_CHIPS:
        data = fetch_from_twelvedata(symbol)
        if data:
            price = data["price"]
            # Calculate change percent from previous day's Firestore value
            yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
            prev_doc = db.collection(PREDICTIONS_COLLECTION).document(f"{symbol}_{yesterday}").get()
            prev_price = prev_doc.to_dict().get("price") if prev_doc.exists else price
            change_pct = ((price - prev_price) / prev_price) * 100 if prev_price else 0
            # Simple signal based on price change (can be enhanced later)
            if change_pct > 1:
                signal = "GOOD"
                explanation = f"Price up {change_pct:.2f}% today"
            elif change_pct < -1:
                signal = "AVOID"
                explanation = f"Price down {change_pct:.2f}% today"
            else:
                signal = "NEUTRAL"
                explanation = "Small change, wait for direction"
            prediction = {
                "symbol": symbol,
                "price": round(price, 2),
                "change_percent": round(change_pct, 2),
                "signal": signal,
                "explanation": explanation,
                "date": datetime.utcnow()
            }
            doc_id = f"{symbol}_{today_str}"
            db.collection(PREDICTIONS_COLLECTION).document(doc_id).set(prediction, merge=True)
            logger.info(f"Updated {symbol}: ₱{price:.2f} ({change_pct:+.2f}%)")
        else:
            logger.warning(f"Twelve Data failed for {symbol}. Keeping last known Firestore value.")
        sleep(1)  # respect rate limit (1 request per second)
    logger.info("Daily update finished.")