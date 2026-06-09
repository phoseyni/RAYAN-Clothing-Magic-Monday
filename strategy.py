import pandas as pd
from config import Config

class Strategy:
    @staticmethod
    def calculate_indicators(ohlcv_data):
        if not ohlcv_data:
            return None

        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['sma_fast'] = df['close'].rolling(window=Config.SMA_FAST).mean()
        df['sma_slow'] = df['close'].rolling(window=Config.SMA_SLOW).mean()
        return df

    @staticmethod
    def calculate_signals(df, entry_price=None):
        if df is None or len(df) < Config.SMA_SLOW:
            return None

        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        current_price = last_row['close']

        # Risk Management: Exit if Stop Loss or Take Profit hit
        if entry_price:
            price_change_pct = (current_price - entry_price) / entry_price
            if price_change_pct <= -Config.STOP_LOSS_PCT:
                return 'sell' # Stop Loss
            if price_change_pct >= Config.TAKE_PROFIT_PCT:
                return 'sell' # Take Profit

        # SMA Crossover Signal (Conservative Trend Following)
        if prev_row['sma_fast'] <= prev_row['sma_slow'] and last_row['sma_fast'] > last_row['sma_slow']:
            return 'buy'
        elif prev_row['sma_fast'] >= prev_row['sma_slow'] and last_row['sma_fast'] < last_row['sma_slow']:
            return 'sell'

        return 'hold'
