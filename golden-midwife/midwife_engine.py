# midwife_engine.py

"""
Golden Midwife Engine v1.0
This module identifies "pregnant stocks" preparing to give birth to strong upward movement.
It evaluates technical, volume, sentiment, and fundamental indicators to score pregnancy potential.
"""

import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="6mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    return data

def calculate_pregnancy_score(data):
    score = 0
    signals = {}

    # Signal 1: Volume Swelling
    avg_vol = data['Volume'].rolling(window=10).mean()
    vol_today = float(data['Volume'].iloc[-1])
    avg_vol_10 = avg_vol.iloc[-1]
    
    if not pd.isna(avg_vol_10) and vol_today > float(avg_vol_10) * 1.5:
        score += 1
        signals['volume_surge'] = True

    
    # Signal 2: Volatility Contraction
    data['daily_range'] = data['High'] - data['Low']
    recent_volatility = data['daily_range'].rolling(window=5).mean()
    prior_volatility = data['daily_range'].rolling(window=20).mean()
    
    vol_5 = recent_volatility.iloc[-1]
    vol_20 = prior_volatility.iloc[-1]
    
    if not pd.isna(vol_5) and not pd.isna(vol_20) and float(vol_5) < float(vol_20) * 0.75:
        score += 1
        signals['volatility_squeeze'] = True
    
    # Signal 3: Price Hugging Resistance
    recent_high = data['Close'].rolling(window=20).max()
    price_now = float(data['Close'].iloc[-1])
    high_20 = recent_high.iloc[-1]
    
    if not pd.isna(high_20) and price_now > float(high_20) * 0.95:
        score += 1
        signals['resistance_hug'] = True

    return score, signals

def analyze_stock(ticker):
    print(f"\n🔍 Analyzing {ticker}...")
    data = fetch_stock_data(ticker)
    score, signals = calculate_pregnancy_score(data)

    print(f"Pregnancy Score: {score}/3")
    for signal, present in signals.items():
        if present:
            print(f"✅ {signal.replace('_', ' ').title()} detected")

# Example use:
if __name__ == "__main__":
    analyze_stock("AAPL")

