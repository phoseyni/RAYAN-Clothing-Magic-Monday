from strategy import Strategy
def test_ema():
    ohlcv = [[0,0,0,0,100,0]]*30 + [[0,0,0,0,150,0]]
    df = Strategy.calculate_indicators(ohlcv)
    assert Strategy.get_signal(df, mode='EMA') == 'buy'
