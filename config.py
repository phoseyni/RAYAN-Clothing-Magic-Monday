import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Alpaca Keys
    API_KEY = os.getenv('ALPACA_API_KEY')
    SECRET = os.getenv('ALPACA_SECRET')
    EXCHANGE_ID = os.getenv('EXCHANGE_ID', 'alpaca')
    SYMBOL = os.getenv('TRADING_SYMBOL', 'BTC/USDT')
    TIMEFRAME = os.getenv('TIMEFRAME', '1h')
    PAPER_TRADING = os.getenv('PAPER_TRADING', 'true').lower() == 'true'

    # Strategy Mode: 'EMA', 'MEAN_REVERSION', 'GRID', 'DCA'
    STRATEGY_MODE = os.getenv('STRATEGY_MODE', 'EMA')

    # Common Parameters
    TRADE_AMOUNT = float(os.getenv('TRADE_AMOUNT', '0.001'))
    STOP_LOSS_PCT = float(os.getenv('STOP_LOSS_PCT', '0.05'))  # Bolder for paper trading
    TAKE_PROFIT_PCT = float(os.getenv('TAKE_PROFIT_PCT', '0.10'))

    # EMA Crossover Parameters
    EMA_FAST = int(os.getenv('EMA_FAST', '12'))
    EMA_SLOW = int(os.getenv('EMA_SLOW', '26'))

    # Mean Reversion (RSI) Parameters
    RSI_PERIOD = int(os.getenv('RSI_PERIOD', '14'))
    RSI_OVERSOLD = int(os.getenv('RSI_OVERSOLD', '30'))
    RSI_OVERBOUGHT = int(os.getenv('RSI_OVERBOUGHT', '70'))

    # Grid Trading Parameters
    GRID_LEVELS = int(os.getenv('GRID_LEVELS', '10'))
    GRID_RANGE_PCT = float(os.getenv('GRID_RANGE_PCT', '0.10'))

    # DCA Parameters
    DCA_INTERVAL_MINUTES = int(os.getenv('DCA_INTERVAL_MINUTES', '1440')) # Default daily
    DCA_AMOUNT = float(os.getenv('DCA_AMOUNT', '0.0001'))

    # Email Configuration
    EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT', 'Pooyan.hoseyni@gmail.com')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'in-v3.mailjet.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
