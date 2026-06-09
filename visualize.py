import matplotlib.pyplot as plt
import pandas as pd
from strategy import Strategy
from config import Config

def plot_strategy(ohlcv_data, signals):
    """
    Plots OHLCV data, indicators and markers for buy/sell signals.
    """
    df = Strategy.calculate_indicators(ohlcv_data)
    if df is None:
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    plt.figure(figsize=(12, 8))

    # Subplot 1: Price and EMAs
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(df.index, df['close'], label='Close Price', color='blue', alpha=0.5)
    if 'ema_fast' in df.columns:
        plt.plot(df.index, df['ema_fast'], label=f'EMA Fast ({Config.EMA_FAST})', color='orange')
    if 'ema_slow' in df.columns:
        plt.plot(df.index, df['ema_slow'], label=f'EMA Slow ({Config.EMA_SLOW})', color='red')

    plt.title(f'Trading Strategy: {Config.SYMBOL} ({Config.TIMEFRAME}) - {Config.STRATEGY_MODE}')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Subplot 2: RSI
    if 'rsi' in df.columns:
        plt.subplot(2, 1, 2, sharex=ax1)
        plt.plot(df.index, df['rsi'], label='RSI', color='purple')
        plt.axhline(Config.RSI_OVERBOUGHT, color='red', linestyle='--')
        plt.axhline(Config.RSI_OVERSOLD, color='green', linestyle='--')
        plt.ylabel('RSI')
        plt.ylim(0, 100)
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.savefig('trading_plot.png')
    plt.close()
