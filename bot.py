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
        self.entry_price = None
        self.position = None

    def run(self):
        logger.info(f"Starting trading bot on {Config.EXCHANGE_ID}...")
        while True:
            try:
                self.tick()
                time.sleep(60)
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

        # 2. Calculate indicators and signal
        df = Strategy.calculate_indicators(ohlcv)
        signal = Strategy.calculate_signals(df, self.entry_price)
        logger.info(f"Generated signal: {signal}")

        # Periodically save a visualization (optional, e.g., every 10 ticks)
        # plot_strategy(ohlcv, [])

        # 3. Execute trade
        if signal == 'buy':
            self.execute_buy(ohlcv[-1][4]) # pass current close price
        elif signal == 'sell':
            self.execute_sell()
        else:
            logger.info("No action taken. Surviving...")

    def execute_buy(self, current_price):
        if self.position == 'long':
            logger.info("Already in a long position.")
            return

        order = self.exchange.create_market_order(Config.SYMBOL, 'buy', Config.TRADE_AMOUNT)
        if order:
            logger.info(f"Buy order executed: {order['id']}")
            self.position = 'long'
            self.entry_price = current_price
            logger.info(f"Entry price set to {self.entry_price}")

    def execute_sell(self):
        if self.position != 'long':
            logger.info("No long position to close.")
            return

        order = self.exchange.create_market_order(Config.SYMBOL, 'sell', Config.TRADE_AMOUNT)
        if order:
            logger.info(f"Sell order executed: {order['id']}")
            self.position = None
            self.entry_price = None
            logger.info("Position closed and entry price cleared.")

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
