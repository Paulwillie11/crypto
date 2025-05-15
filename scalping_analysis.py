import requests
import pandas as pd
import numpy as np

def get_klines(symbol="SIGNUSDT", interval="15m", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df

def compute_indicators(df):
    df["SMA20"] = df["close"].rolling(window=20).mean()
    df["EMA20"] = df["close"].ewm(span=20).mean()

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    df["EMA12"] = df["close"].ewm(span=12).mean()
    df["EMA26"] = df["close"].ewm(span=26).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=9).mean()
    df["MACD_hist"] = df["MACD"] - df["Signal"]

    return df

def analyze_trend(df):
    latest = df.iloc[-1]
    trend = "Sideways"

    if latest["EMA20"] > latest["SMA20"] and latest["RSI"] > 55 and latest["MACD"] > latest["Signal"]:
        trend = "Uptrend"
    elif latest["EMA20"] < latest["SMA20"] and latest["RSI"] < 45 and latest["MACD"] < latest["Signal"]:
        trend = "Downtrend"

    return trend

if __name__ == "__main__":
    timeframes = ["5m", "15m", "1h", "4h", "1d"]
    score = 0

    print("SIGN/USDT Trend Analysis:")
    print("-" * 40)

    for tf in timeframes:
        try:
            df = get_klines(interval=tf)
            df = compute_indicators(df)
            trend = analyze_trend(df)
            print(f"{tf.upper():<5}: {trend}")
            if tf in ["5m", "15m", "1h"] and trend == "Uptrend":
                score += 1
        except Exception as e:
            print(f"{tf.upper():<5}: Error - {e}")

    print("-" * 40)
    if score >= 3:
        print("SCALPING SIGNAL: Enter now")
    else:
        print("SCALPING SIGNAL: Wait for better entry")
