import pandas as pd
import pandas_ta as ta
from binance.client import Client
from binance.exceptions import BinanceAPIException
import time

# Add your Binance API keys if needed (only if you're making private calls)
# client = Client(api_key='your_api_key', api_secret='your_api_secret')
client = Client()

def get_klines(symbol, interval, limit=100):
    try:
        data = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
        ])
        df['close'] = pd.to_numeric(df['close'])
        return df
    except BinanceAPIException as e:
        print(f"Binance API error: {e.message}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def analyze(df):
    if df.empty or len(df) < 50:
        return "Insufficient data"

    df['EMA50'] = ta.ema(df['close'], length=50)
    df['EMA200'] = ta.ema(df['close'], length=200)
    df['RSI'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])

    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']

    last = -1

    try:
        price = df['close'].iloc[last]
        ema50 = df['EMA50'].iloc[last]
        ema200 = df['EMA200'].iloc[last]
        rsi = df['RSI'].iloc[last]
        macd_val = df['MACD'].iloc[last]
        macd_signal = df['MACD_signal'].iloc[last]
    except IndexError:
        return "Indexing error: Possibly not enough rows"

    if price > ema50 and price > ema200 and macd_val > macd_signal and rsi > 50:
        return "Uptrend (Strong)"
    elif price < ema50 and price < ema200 and macd_val < macd_signal and rsi < 50:
        return "Downtrend (Strong)"
    else:
        return "Sideways / Weak Signal"

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]

intervals = ["15m", "1h", "4h", "1d"]

for symbol in symbols:
    print(f"\n===== {symbol} Analysis =====")
    for interval in intervals:
        df = get_klines(symbol, interval)
        trend = analyze(df)
        print(f"  {interval}: {trend}")
        time.sleep(1)  # avoid rate limiting
