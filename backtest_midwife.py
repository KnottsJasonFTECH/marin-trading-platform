# backtest_midwife.py

"""
Golden Midwife Backtest Engine v1.0
Scans AAPL historical data for pregnancy signals (volume surge, volatility squeeze, resistance hug),
then tracks price performance after each signal day to measure predictive strength.
"""

import yfinance as yf
import pandas as pd

def fetch_data(ticker="AAPL", period="6mo", interval="1d"):
    return yf.download(ticker, period=period, interval=interval)

def apply_signals(data):
    data['avg_vol_10'] = data['Volume'].rolling(window=10).mean()
    data['vol_surge'] = (data['Volume'] > data['avg_vol_10'] * 1.5)

    data['daily_range'] = data['High'] - data['Low']
    data['vol_5'] = data['daily_range'].rolling(window=5).mean()
    data['vol_20'] = data['daily_range'].rolling(window=20).mean()
    data['vol_squeeze'] = (data['vol_5'] < data['vol_20'] * 0.75)

    data['recent_high'] = data['Close'].rolling(window=20).max()
    data['resistance_hug'] = (data['Close'] > data['recent_high'] * 0.95)

    data['pregnancy_score'] = (
        data['vol_surge'].fillna(False).astype(int) +
        data['vol_squeeze'].fillna(False).astype(int) +
        data['resistance_hug'].fillna(False).astype(int)
    )
    return data

def analyze_forward_returns(data, forward_days=[3, 5]):
    results = []

    for i in range(len(data) - max(forward_days)):
        row = data.iloc[i]
        if row['pregnancy_score'] > 0:
            entry_price = row['Close']
            forward_data = data.iloc[i+1 : i+1+max(forward_days)]

            result = {
                "date": row.name,
                "score": row['pregnancy_score'],
                "vol_surge": row['vol_surge'],
                "vol_squeeze": row['vol_squeeze'],
                "resistance_hug": row['resistance_hug'],
                "entry_price": entry_price,
            }

            for d in forward_days:
                future_price = forward_data.iloc[d-1]['Close']
                return_pct = ((future_price - entry_price) / entry_price) * 100
                result[f"return_{d}d_pct"] = return_pct

            results.append(result)

    return pd.DataFrame(results)

def main():
    data = fetch_data()
    data = apply_signals(data)
    results = analyze_forward_returns(data)

    results.to_csv("midwife_backtest_results.csv", index=False)
    print("Backtest complete. Results saved to 'midwife_backtest_results.csv'.")

if __name__ == "__main__":
    main()
