import requests
import time
from dotenv import load_dotenv

load_dotenv()

BLUE_CHIPS = ["AC", "SM", "BDO", "JFC", "TEL", "MER", "GLO", "ALI", "AEV", "MBT"]

def get_real_stock_price(symbol):
    """Fetch real stock price for a PSE symbol using the free Phisix API."""
    url = f"http://phisix-api3.appspot.com/stocks/{symbol}.json"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        # The correct key is "stocks" (list)
        if data and "stocks" in data and data["stocks"]:
            stock_data = data["stocks"][0]
            price = float(stock_data["price"]["amount"])
            percent_change = float(stock_data["percentChange"])
            return price, percent_change, True
        else:
            print(f"No data for {symbol}")
            return None, None, False
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None, None, False

def get_all_prices():
    results = {}
    for symbol in BLUE_CHIPS:
        price, change, success = get_real_stock_price(symbol)
        if success:
            results[symbol] = {"price": price, "change": change, "success": True}
        else:
            results[symbol] = {"success": False}
        time.sleep(0.5)
    return results