import ccxt
import logging
from config import Config

logger = logging.getLogger(__name__)

class ExchangeInterface:
    def __init__(self):
        try:
            exchange_class = getattr(ccxt, Config.EXCHANGE_ID)
            self.exchange = exchange_class({
                'apiKey': Config.API_KEY,
                'secret': Config.SECRET,
                'enableRateLimit': True,
            })
            logger.info(f"Initialized {Config.EXCHANGE_ID} exchange.")
        except AttributeError:
            logger.error(f"Exchange {Config.EXCHANGE_ID} not found in CCXT.")
            raise

    def fetch_ohlcv(self, symbol, timeframe, limit=100):
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol}: {e}")
            return None

    def fetch_balance(self):
        try:
            return self.exchange.fetch_balance()
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return None

    def create_market_order(self, symbol, side, amount):
        try:
            logger.info(f"Creating {side} market order for {amount} {symbol}")
            return self.exchange.create_market_order(symbol, side, amount)
        except Exception as e:
            logger.error(f"Error creating market order: {e}")
            return None

    def fetch_ticker(self, symbol):
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return None
