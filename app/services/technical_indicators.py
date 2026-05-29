import pandas as pd
import ta

def calculate_sma(prices, window):
    """Calculate Simple Moving Average"""
    if len(prices) < window:
        return None
    return list(pd.Series(prices).rolling(window=window).mean())

def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index (last value)"""
    if len(prices) < period + 1:
        return None
    return ta.momentum.RSIIndicator(pd.Series(prices), window=period).rsi().iloc[-1]

def calculate_macd(prices):
    """Calculate MACD line, signal line, histogram (last values)"""
    if len(prices) < 26:
        return None
    macd_indicator = ta.trend.MACD(pd.Series(prices))
    macd_line = macd_indicator.macd().iloc[-1]
    signal_line = macd_indicator.macd_signal().iloc[-1]
    histogram = macd_indicator.macd_diff().iloc[-1]
    return {
        "macd_line": macd_line,
        "signal_line": signal_line,
        "histogram": histogram,
        "bullish": macd_line > signal_line,
        "bearish": macd_line < signal_line
    }