import ccxt
import logging
from config import Config

logger = logging.getLogger(__name__)

class ExchangeInterface:
    def __init__(self):
        try:
            exchange_class = getattr(ccxt, Config.EXCHANGE_ID)
            self.exchange = exchange_class({'apiKey': Config.API_KEY, 'secret': Config.SECRET})
            if Config.EXCHANGE_ID == 'alpaca' and Config.PAPER_TRADING:
                self.exchange.set_sandbox_mode(True)
            logger.info(f"Initialized {Config.EXCHANGE_ID} exchange.")
        except Exception as e:
            logger.error(f"Init error: {e}")
            raise

    def fetch_ohlcv(self, symbol, timeframe, limit=100):
        try: return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        except Exception as e: logger.error(f"OHLCV error: {e}"); return None

    def fetch_balance(self):
        try: return self.exchange.fetch_balance()
        except Exception as e: logger.error(f"Balance error: {e}"); return None

    def create_market_order(self, symbol, side, amount):
        try:
            logger.info(f"Market {side} {amount} {symbol}")
            return self.exchange.create_market_order(symbol, side, amount)
        except Exception as e: logger.error(f"Order error: {e}"); return None

    def fetch_ticker(self, symbol):
        try: return self.exchange.fetch_ticker(symbol)
        except Exception as e: logger.error(f"Ticker error: {e}"); return None
