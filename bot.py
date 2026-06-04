import time
import logging
from config import Config
from exchange_interface import ExchangeInterface
from strategy import Strategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self):
        self.exchange = ExchangeInterface()
        self.position = None  # To track current position (simulated for simplicity)

    def run(self):
        logger.info("Starting trading bot...")
        while True:
            try:
                self.tick()
                # Sleep based on timeframe or a fixed interval
                time.sleep(60) # Check every minute
            except KeyboardInterrupt:
                logger.info("Bot stopped by user.")
                break
            except Exception as e:
                logger.error(f"Unexpected error in bot loop: {e}")
                time.sleep(30)

    def tick(self):
        logger.info(f"Checking markets for {Config.SYMBOL}...")

        # 1. Fetch data
        ohlcv = self.exchange.fetch_ohlcv(Config.SYMBOL, Config.TIMEFRAME)
        if not ohlcv:
            return

        # 2. Calculate signal
        signal = Strategy.calculate_signals(ohlcv)
        logger.info(f"Generated signal: {signal}")

        # 3. Execute trade
        if signal == 'buy':
            self.execute_buy()
        elif signal == 'sell':
            self.execute_sell()
        else:
            logger.info("No action taken.")

    def execute_buy(self):
        if self.position == 'long':
            logger.info("Already in a long position.")
            return

        order = self.exchange.create_market_order(Config.SYMBOL, 'buy', Config.TRADE_AMOUNT)
        if order:
            logger.info(f"Buy order executed: {order['id']}")
            self.position = 'long'

    def execute_sell(self):
        if self.position != 'long':
            logger.info("No long position to close.")
            return

        order = self.exchange.create_market_order(Config.SYMBOL, 'sell', Config.TRADE_AMOUNT)
        if order:
            logger.info(f"Sell order executed: {order['id']}")
            self.position = None

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
