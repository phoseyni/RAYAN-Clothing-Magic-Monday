import pandas as pd
import numpy as np
from config import Config

class Strategy:
    @staticmethod
    def calculate_indicators(ohlcv_data):
        if not ohlcv_data:
            return None
        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['ema_fast'] = df['close'].ewm(span=Config.EMA_FAST, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=Config.EMA_SLOW, adjust=False).mean()
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=Config.RSI_PERIOD).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=Config.RSI_PERIOD).mean()
        rs = gain / (loss + 1e-9)
        df['rsi'] = 100 - (100 / (1 + rs))
        return df

    @staticmethod
    def get_signal(df, entry_price=None, mode=Config.STRATEGY_MODE):
        if df is None or len(df) < max(Config.EMA_SLOW, Config.RSI_PERIOD):
            return None
        last_row, prev_row = df.iloc[-1], df.iloc[-2]
        current_price = last_row['close']
        if entry_price:
            pnl = (current_price - entry_price) / entry_price
            if pnl <= -Config.STOP_LOSS_PCT or pnl >= Config.TAKE_PROFIT_PCT:
                return 'sell'
        if mode == 'EMA':
            if prev_row['ema_fast'] <= prev_row['ema_slow'] and last_row['ema_fast'] > last_row['ema_slow']:
                return 'buy'
            if prev_row['ema_fast'] >= prev_row['ema_slow'] and last_row['ema_fast'] < last_row['ema_slow']:
                return 'sell'
        elif mode == 'MEAN_REVERSION':
            if last_row['rsi'] < Config.RSI_OVERSOLD:
                return 'buy'
            if last_row['rsi'] > Config.RSI_OVERBOUGHT:
                return 'sell'
        elif mode == 'DCA':
            return 'buy'
        return 'hold'

    @staticmethod
    def get_grid_levels(current_price):
        range_val = current_price * Config.GRID_RANGE_PCT
        return np.linspace(current_price - range_val/2, current_price + range_val/2, Config.GRID_LEVELS)
