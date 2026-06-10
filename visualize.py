import matplotlib.pyplot as plt
import pandas as pd
from strategy import Strategy
from config import Config

def plot_strategy(ohlcv_data, signals):
    df = Strategy.calculate_indicators(ohlcv_data)
    if df is None:
        return
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    plt.figure(figsize=(12, 8))
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(df.index, df['close'], label='Price', color='blue', alpha=0.5)
    if 'ema_fast' in df.columns:
        plt.plot(df.index, df['ema_fast'], label='EMA Fast', color='orange')
    if 'ema_slow' in df.columns:
        plt.plot(df.index, df['ema_slow'], label='EMA Slow', color='red')
    plt.title(f'Strategy: {Config.SYMBOL} - {Config.STRATEGY_MODE} v{Config.VERSION}')
    plt.legend()
    plt.grid(True)
    if 'rsi' in df.columns:
        plt.subplot(2, 1, 2, sharex=ax1)
        plt.plot(df.index, df['rsi'], label='RSI', color='purple')
        plt.axhline(Config.RSI_OVERBOUGHT, color='red', linestyle='--')
        plt.axhline(Config.RSI_OVERSOLD, color='green', linestyle='--')
        plt.ylim(0, 100)
        plt.legend()
        plt.grid(True)
    plt.tight_layout()
    plt.savefig('trading_plot.png')
    plt.close()
