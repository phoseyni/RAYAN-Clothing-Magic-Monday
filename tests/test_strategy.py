from strategy import Strategy
from config import Config

def test_calculate_signals_buy():
    # Mock OHLCV data where fast SMA crosses above slow SMA at the last candle
    ohlcv_data = []
    # 30 candles of 100
    for i in range(30):
        ohlcv_data.append([0, 0, 0, 0, 100, 0])
    # 31st candle of 200
    ohlcv_data.append([0, 0, 0, 0, 200, 0])

    signal = Strategy.calculate_signals(ohlcv_data)
    assert signal == 'buy'

def test_calculate_signals_sell():
    # Mock OHLCV data where fast SMA crosses below slow SMA at the last candle
    ohlcv_data = []
    # 30 candles of 100
    for i in range(30):
        ohlcv_data.append([0, 0, 0, 0, 100, 0])
    # 31st candle of 50
    ohlcv_data.append([0, 0, 0, 0, 50, 0])

    signal = Strategy.calculate_signals(ohlcv_data)
    assert signal == 'sell'

def test_calculate_signals_hold():
    # Mock OHLCV data where no crossover occurs
    ohlcv_data = []
    for i in range(35):
        ohlcv_data.append([0, 0, 0, 0, 100, 0])

    signal = Strategy.calculate_signals(ohlcv_data)
    assert signal == 'hold'

def test_calculate_signals_insufficient_data():
    ohlcv_data = [[0,0,0,0,100,0]] * (Config.SMA_SLOW - 1)
    signal = Strategy.calculate_signals(ohlcv_data)
    assert signal is None
