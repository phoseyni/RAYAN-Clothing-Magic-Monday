import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('ALPACA_API_KEY')
    SECRET = os.getenv('ALPACA_SECRET')
    # CCXT uses 'alpaca' for Alpaca
    EXCHANGE_ID = os.getenv('EXCHANGE_ID', 'alpaca')
    SYMBOL = os.getenv('TRADING_SYMBOL', 'BTC/USDT') # Alpaca Crypto usually uses USD or USDT
    TIMEFRAME = os.getenv('TIMEFRAME', '1h')
    SMA_FAST = int(os.getenv('SMA_FAST', '10'))
    SMA_SLOW = int(os.getenv('SMA_SLOW', '30'))
    TRADE_AMOUNT = float(os.getenv('TRADE_AMOUNT', '0.001'))

    # Risk Management: Survive and win little by little
    STOP_LOSS_PCT = float(os.getenv('STOP_LOSS_PCT', '0.02'))  # 2% stop loss
    TAKE_PROFIT_PCT = float(os.getenv('TAKE_PROFIT_PCT', '0.04')) # 4% take profit

    # Alpaca Paper Trading URL (default)
    PAPER_TRADING = os.getenv('PAPER_TRADING', 'true').lower() == 'true'
