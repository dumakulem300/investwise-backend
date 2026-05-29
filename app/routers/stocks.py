from fastapi import APIRouter, HTTPException
from app.services.stock_service import get_latest_predictions_from_firestore, BLUE_CHIPS, get_all_predictions, save_predictions_to_firestore
from app.services.technical_indicators import calculate_sma, calculate_rsi, calculate_macd
import pandas as pd
import yfinance as yf

router = APIRouter(prefix="/stocks", tags=["stocks"])

@router.get("/")
async def get_predictions():
    """Get cached predictions from Firestore."""
    predictions = get_latest_predictions_from_firestore()
    return {"stocks": predictions}

@router.get("/chart/{symbol}")
async def get_chart_data(symbol: str):
    """Return OHLCV + indicators for charting (live data)."""
    if symbol not in BLUE_CHIPS:
        raise HTTPException(status_code=404, detail="Symbol not in blue chip list")
    
    ticker = yf.Ticker(f"{symbol}.PS")
    df = ticker.history(period="6mo")
    if df.empty:
        # try fallback format
        ticker = yf.Ticker(f"PSE:{symbol}")
        df = ticker.history(period="6mo")
    if df.empty:
        raise HTTPException(status_code=404, detail="No data for symbol")
    
    df.index = df.index.tz_localize(None)
    dates = df.index.strftime("%Y-%m-%d").tolist()
    
    ohlcv = {
        "open": df['Open'].tolist(),
        "high": df['High'].tolist(),
        "low": df['Low'].tolist(),
        "close": df['Close'].tolist(),
        "volume": df['Volume'].tolist()
    }
    
    closes = df['Close'].tolist()
    sma20 = None
    if len(closes) >= 20:
        sma20 = pd.Series(closes).rolling(20).mean().tolist()
    sma50 = None
    if len(closes) >= 50:
        sma50 = pd.Series(closes).rolling(50).mean().tolist()
    
    rsi_list = None
    if len(closes) >= 14:
        rsi_indicator = pd.Series(closes).rolling(14).apply(lambda x: calculate_rsi(x.tolist(), 14), raw=False)
        rsi_list = rsi_indicator.tolist()
    
    macd_line = None
    signal_line = None
    histogram = None
    if len(closes) >= 26:
        macd_vals = []
        signal_vals = []
        hist_vals = []
        for i in range(26, len(closes)+1):
            macd = calculate_macd(closes[:i])
            if macd:
                macd_vals.append(macd['macd_line'])
                signal_vals.append(macd['signal_line'])
                hist_vals.append(macd['histogram'])
            else:
                macd_vals.append(None)
                signal_vals.append(None)
                hist_vals.append(None)
        macd_line = [None]*25 + macd_vals
        signal_line = [None]*25 + signal_vals
        histogram = [None]*25 + hist_vals
    
    return {
        "symbol": symbol,
        "dates": dates,
        "ohlcv": ohlcv,
        "sma20": sma20,
        "sma50": sma50,
        "rsi": rsi_list,
        "macd": {
            "macd_line": macd_line,
            "signal_line": signal_line,
            "histogram": histogram
        }
    }