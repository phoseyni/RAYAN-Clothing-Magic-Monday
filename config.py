import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('EXCHANGE_API_KEY')
    SECRET = os.getenv('EXCHANGE_SECRET')
    EXCHANGE_ID = os.getenv('EXCHANGE_ID', 'kraken')  # Defaulting to Kraken as a European broker
    SYMBOL = os.getenv('TRADING_SYMBOL', 'BTC/EUR')
    TIMEFRAME = os.getenv('TIMEFRAME', '1h')
    SMA_FAST = int(os.getenv('SMA_FAST', '10'))
    SMA_SLOW = int(os.getenv('SMA_SLOW', '30'))
    TRADE_AMOUNT = float(os.getenv('TRADE_AMOUNT', '0.001'))
