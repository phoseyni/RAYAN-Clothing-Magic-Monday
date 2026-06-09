from strategy import Strategy
from config import Config

def test_ema_crossover_buy():
    # Price crosses up to trigger EMA crossover
    ohlcv = [[0, 0, 0, 0, 100, 0]] * 30 + [[0, 0, 0, 0, 150, 0]]
    df = Strategy.calculate_indicators(ohlcv)
    signal = Strategy.get_signal(df, mode='EMA')
    assert signal == 'buy'

def test_rsi_mean_reversion_buy():
    # RSI < 30 (Oversold) - Needs more data for RSI to stabilize
    ohlcv = [[0, 0, 0, 0, 100, 0]] * 30 + [[0, 0, 0, 0, 50, 0]] * 10
    df = Strategy.calculate_indicators(ohlcv)
    assert df.iloc[-1]['rsi'] < 30
    signal = Strategy.get_signal(df, mode='MEAN_REVERSION')
    assert signal == 'buy'

def test_rsi_mean_reversion_sell():
    # RSI > 70 (Overbought)
    ohlcv = [[0, 0, 0, 0, 100, 0]] * 30 + [[0, 0, 0, 0, 150, 0]] * 10
    df = Strategy.calculate_indicators(ohlcv)
    assert df.iloc[-1]['rsi'] > 70
    signal = Strategy.get_signal(df, mode='MEAN_REVERSION')
    assert signal == 'sell'

def test_stop_loss():
    ohlcv = [[0, 0, 0, 0, 100, 0]] * 35
    df = Strategy.calculate_indicators(ohlcv)
    # Entry 110, Current 100 -> ~9% loss. Stop loss is 5%
    signal = Strategy.get_signal(df, entry_price=110, mode='EMA')
    assert signal == 'sell'

def test_grid_levels():
    levels = Strategy.get_grid_levels(60000)
    assert len(levels) == Config.GRID_LEVELS
    assert levels[0] < 60000
    assert levels[-1] > 60000
