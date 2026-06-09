import matplotlib.pyplot as plt
import pandas as pd
from strategy import Strategy
from exchange_interface import ExchangeInterface
from config import Config

def generate_visualization():
    """
    Fetches real data and generates a strategy plot.
    """
    print(f"Generating visualization for {Config.SYMBOL}...")
    exchange = ExchangeInterface()
    ohlcv = exchange.fetch_ohlcv(Config.SYMBOL, Config.TIMEFRAME, limit=100)

    if not ohlcv:
        print("Failed to fetch data for visualization.")
        return

    df = Strategy.calculate_indicators(ohlcv)
    if df is None:
        print("Insufficient data for plotting.")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close'], label='Close Price', color='blue', alpha=0.5)
    plt.plot(df.index, df['sma_fast'], label='SMA Fast (10)', color='orange')
    plt.plot(df.index, df['sma_slow'], label='SMA Slow (30)', color='red')

    plt.title(f'Alpaca Trading Strategy: {Config.SYMBOL} ({Config.TIMEFRAME})')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    output_file = 'trading_plot.png'
    plt.savefig(output_file)
    print(f"Plot successfully saved to {output_file}")

if __name__ == "__main__":
    generate_visualization()
