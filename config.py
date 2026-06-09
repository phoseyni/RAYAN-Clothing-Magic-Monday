import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('ALPACA_API_KEY')
    SECRET = os.getenv('ALPACA_SECRET')
    EXCHANGE_ID = os.getenv('EXCHANGE_ID', 'alpaca')
    SYMBOL = os.getenv('TRADING_SYMBOL', 'BTC/USDT')
    TIMEFRAME = os.getenv('TIMEFRAME', '1h')
    SMA_FAST = int(os.getenv('SMA_FAST', '10'))
    SMA_SLOW = int(os.getenv('SMA_SLOW', '30'))
    TRADE_AMOUNT = float(os.getenv('TRADE_AMOUNT', '0.001'))

    STOP_LOSS_PCT = float(os.getenv('STOP_LOSS_PCT', '0.02'))
    TAKE_PROFIT_PCT = float(os.getenv('TAKE_PROFIT_PCT', '0.04'))

    PAPER_TRADING = os.getenv('PAPER_TRADING', 'true').lower() == 'true'

    # Email Configuration
    EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT', 'Pooyan.hoseyni@gmail.com')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'in-v3.mailjet.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
