import requests
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BLUE_CHIPS = ["AC", "SM", "BDO", "JFC", "TEL", "MER", "GLO", "ALI", "AEV", "MBT"]

def get_real_stock_price(symbol):
    """Fetch real stock price for a PSE symbol using the free Phisix API."""
    url = f"http://phisix-api3.appspot.com/stocks/{symbol}.json"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Phisix API returned {resp.status_code} for {symbol}")
            return None, None, False
        data = resp.json()
        if data and "stock" in data and data["stock"]:
            stock_data = data["stock"][0]
            price = float(stock_data["price"]["amount"])
            percent_change = float(stock_data["percent_change"])
            logger.info(f"Phisix success {symbol}: ₱{price}")
            return price, percent_change, True
        else:
            logger.warning(f"No stock data for {symbol}")
            return None, None, False
    except Exception as e:
        logger.error(f"Error fetching {symbol}: {e}")
        return None, None, False

def get_all_prices():
    """Return dict of symbol -> {price, change, success}. If API fails, returns None for price."""
    results = {}
    for symbol in BLUE_CHIPS:
        price, change, success = get_real_stock_price(symbol)
        if success:
            results[symbol] = {"price": price, "change": change, "success": True}
        else:
            results[symbol] = {"success": False, "price": None, "change": None}
        time.sleep(0.5)  # rate limit
    return results
