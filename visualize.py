import matplotlib.pyplot as plt
import pandas as pd
from strategy import Strategy

def plot_strategy(ohlcv_data, signals):
    """
    Plots OHLCV data, SMAs and markers for buy/sell signals.
    """
    df = Strategy.calculate_indicators(ohlcv_data)
    if df is None:
        print("Insufficient data for plotting.")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close'], label='Close Price', color='blue', alpha=0.5)
    plt.plot(df.index, df['sma_fast'], label='SMA Fast', color='orange')
    plt.plot(df.index, df['sma_slow'], label='SMA Slow', color='red')

    # Plot Buy/Sell signals if provided (simplified for visualization)
    # In a real bot, we'd record actual trade timestamps

    plt.title('Trading Strategy Visualization')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Save to file as we are in a headless environment
    plt.savefig('trading_plot.png')
    print("Plot saved to trading_plot.png")

if __name__ == "__main__":
    # Example usage with mock data if needed
    pass
