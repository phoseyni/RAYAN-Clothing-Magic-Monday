from strategy import Strategy

def test_calculate_signals_buy():
    ohlcv_data = [[0, 0, 0, 0, 100, 0]] * 30 + [[0, 0, 0, 0, 200, 0]]
    df = Strategy.calculate_indicators(ohlcv_data)
    signal = Strategy.calculate_signals(df)
    assert signal == 'buy'

def test_calculate_signals_sell():
    ohlcv_data = [[0, 0, 0, 0, 100, 0]] * 30 + [[0, 0, 0, 0, 50, 0]]
    df = Strategy.calculate_indicators(ohlcv_data)
    signal = Strategy.calculate_signals(df)
    assert signal == 'sell'

def test_stop_loss():
    # 35 candles at 100
    ohlcv_data = [[0, 0, 0, 0, 100, 0]] * 35
    df = Strategy.calculate_indicators(ohlcv_data)
    # Entry price 110, Current price 100 -> ~9% drop, should trigger SL (Config.STOP_LOSS_PCT is 0.02)
    signal = Strategy.calculate_signals(df, entry_price=110)
    assert signal == 'sell'

def test_take_profit():
    # 35 candles at 100
    ohlcv_data = [[0, 0, 0, 0, 100, 0]] * 35
    df = Strategy.calculate_indicators(ohlcv_data)
    # Entry price 90, Current price 100 -> ~11% gain, should trigger TP (Config.TAKE_PROFIT_PCT is 0.04)
    signal = Strategy.calculate_signals(df, entry_price=90)
    assert signal == 'sell'
