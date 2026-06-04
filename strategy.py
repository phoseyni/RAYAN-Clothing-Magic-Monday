import pandas as pd
from config import Config

class Strategy:
    @staticmethod
    def calculate_signals(ohlcv_data):
        if not ohlcv_data:
            return None

        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['sma_fast'] = df['close'].rolling(window=Config.SMA_FAST).mean()
        df['sma_slow'] = df['close'].rolling(window=Config.SMA_SLOW).mean()

        if len(df) < Config.SMA_SLOW:
            return None

        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        # SMA Crossover Signal
        if prev_row['sma_fast'] <= prev_row['sma_slow'] and last_row['sma_fast'] > last_row['sma_slow']:
            return 'buy'
        elif prev_row['sma_fast'] >= prev_row['sma_slow'] and last_row['sma_fast'] < last_row['sma_slow']:
            return 'sell'

        return 'hold'
