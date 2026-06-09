from strategy import Strategy
from config import Config

def test_ema_crossover():
    # Price jump triggers EMA cross
    ohlcv = [[0, 0, 0, 0, 100, 0]] * 30 + [[0, 0, 0, 0, 150, 0]]
    df = Strategy.calculate_indicators(ohlcv)
    assert Strategy.get_signal(df, mode='EMA') == 'buy'

def test_rsi_mean_reversion():
    # Flat price followed by drop
    ohlcv = [[0, 0, 0, 0, 100, 0]] * 30 + [[0, 0, 0, 0, 50, 0]] * 10
    df = Strategy.calculate_indicators(ohlcv)
    assert df.iloc[-1]['rsi'] < 30
    assert Strategy.get_signal(df, mode='MEAN_REVERSION') == 'buy'

def test_stop_loss():
    ohlcv = [[0, 0, 0, 0, 100, 0]] * 35
    df = Strategy.calculate_indicators(ohlcv)
    # Entry 110, Price 100 -> ~9% loss. Default SL is 5% (0.05)
    assert Strategy.get_signal(df, entry_price=110, mode='EMA') == 'sell'
