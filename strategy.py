import pandas as pd
import numpy as np
from config import Config

class Strategy:
    @staticmethod
    def calculate_indicators(ohlcv_data):
        if not ohlcv_data:
            return None

        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # EMA
        df['ema_fast'] = df['close'].ewm(span=Config.EMA_FAST, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=Config.EMA_SLOW, adjust=False).mean()

        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=Config.RSI_PERIOD).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=Config.RSI_PERIOD).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        return df

    @staticmethod
    def get_signal(df, entry_price=None, mode=Config.STRATEGY_MODE):
        if df is None or len(df) < max(Config.EMA_SLOW, Config.RSI_PERIOD):
            return None

        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        current_price = last_row['close']

        # Global Risk Management
        if entry_price:
            pnl_pct = (current_price - entry_price) / entry_price
            if pnl_pct <= -Config.STOP_LOSS_PCT:
                return 'sell' # Stop Loss
            if pnl_pct >= Config.TAKE_PROFIT_PCT:
                return 'sell' # Take Profit

        if mode == 'EMA':
            if prev_row['ema_fast'] <= prev_row['ema_slow'] and last_row['ema_fast'] > last_row['ema_slow']:
                return 'buy'
            elif prev_row['ema_fast'] >= prev_row['ema_slow'] and last_row['ema_fast'] < last_row['ema_slow']:
                return 'sell'

        elif mode == 'MEAN_REVERSION':
            if last_row['rsi'] < Config.RSI_OVERSOLD:
                return 'buy'
            elif last_row['rsi'] > Config.RSI_OVERBOUGHT:
                return 'sell'

        elif mode == 'DCA':
            # DCA usually just buys at intervals, but we can add a simple condition
            return 'buy'

        return 'hold'

    @staticmethod
    def get_grid_levels(current_price):
        range_val = current_price * Config.GRID_RANGE_PCT
        lower_bound = current_price - (range_val / 2)
        upper_bound = current_price + (range_val / 2)
        return np.linspace(lower_bound, upper_bound, Config.GRID_LEVELS)
