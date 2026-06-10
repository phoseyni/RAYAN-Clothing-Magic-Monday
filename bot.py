import time
import logging
import sys
import os
from config import Config
from exchange_interface import ExchangeInterface
from strategy import Strategy
from visualize import plot_strategy
from email_notifier import EmailNotifier

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

def pre_flight_check():
    """Validates the environment and configuration before starting the bot."""
    logger.info("Performing pre-flight checks...")

    # 1. Check for .env file
    if not os.path.exists('.env'):
        logger.error("CRITICAL ERROR: '.env' file not found! Please run 'cp .env.template .env' and fill in your keys.")
        return False

    # 2. Check for Alpaca Keys
    if not Config.API_KEY or not Config.SECRET or Config.API_KEY == "your_key":
        logger.error("CRITICAL ERROR: Alpaca API keys are missing or invalid in .env!")
        return False

    # 3. Check for Email Keys (Optional but recommended)
    if not Config.SMTP_USER or not Config.SMTP_PASSWORD:
        logger.warning("Email notifications are disabled (SMTP credentials missing).")

    logger.info(f"Pre-flight checks passed. Target: {Config.EXCHANGE_ID} ({Config.SYMBOL})")
    return True

class TradingBot:
    def __init__(self):
        try:
            self.exchange = ExchangeInterface()
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {e}")
            raise
        self.entry_price = None
        self.position = None
        self.last_dca_time = 0

    def run(self):
        logger.info(f"Starting trading bot v{Config.VERSION} on {Config.EXCHANGE_ID} in {Config.STRATEGY_MODE} mode...")
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

        # 2. Strategy Specific Execution
        if Config.STRATEGY_MODE == 'DCA':
            self.handle_dca()
            return

        # Default Strategy Handling (EMA, MEAN_REVERSION)
        df = Strategy.calculate_indicators(ohlcv)
        signal = Strategy.get_signal(df, self.entry_price)
        logger.info(f"Generated signal: {signal}")

        # 3. Execute trade
        if signal == 'buy':
            self.execute_buy(ohlcv)
        elif signal == 'sell':
            self.execute_sell(ohlcv)

    def handle_dca(self):
        current_time = time.time()
        if current_time - self.last_dca_time >= (Config.DCA_INTERVAL_MINUTES * 60):
            logger.info("Executing DCA Buy...")
            order = self.exchange.create_market_order(Config.SYMBOL, 'buy', Config.DCA_AMOUNT)
            if order:
                self.last_dca_time = current_time
                EmailNotifier.send_trade_notification(
                    subject=f"DCA BUY executed: {Config.SYMBOL}",
                    body=f"Amount: {Config.DCA_AMOUNT}\nTime: {time.ctime()}\nBot Version: {Config.VERSION}"
                )

    def execute_buy(self, ohlcv):
        if self.position == 'long':
            return

        current_price = ohlcv[-1][4]
        order = self.exchange.create_market_order(Config.SYMBOL, 'buy', Config.TRADE_AMOUNT)
        if order:
            logger.info(f"Buy order executed: {order['id']}")
            self.position = 'long'
            self.entry_price = current_price

            plot_strategy(ohlcv, [])
            EmailNotifier.send_trade_notification(
                subject=f"TRADE OPENED ({Config.STRATEGY_MODE}): Buy {Config.SYMBOL}",
                body=f"Price: {current_price}\nTime: {time.ctime()}\nBot Version: {Config.VERSION}",
                attachment_path="trading_plot.png"
            )

    def execute_sell(self, ohlcv):
        if self.position != 'long':
            return

        current_price = ohlcv[-1][4]
        order = self.exchange.create_market_order(Config.SYMBOL, 'sell', Config.TRADE_AMOUNT)
        if order:
            logger.info(f"Sell order executed: {order['id']}")
            pnl_pct = (current_price - self.entry_price) / self.entry_price * 100

            plot_strategy(ohlcv, [])
            EmailNotifier.send_trade_notification(
                subject=f"TRADE CLOSED ({Config.STRATEGY_MODE}): Sell {Config.SYMBOL}",
                body=f"Price: {current_price}\nPNL: {pnl_pct:.2f}%\nTime: {time.ctime()}\nBot Version: {Config.VERSION}",
                attachment_path="trading_plot.png"
            )

            self.position = None
            self.entry_price = None

if __name__ == "__main__":
    if pre_flight_check():
        try:
            bot = TradingBot()
            bot.run()
        except Exception as e:
            logger.critical(f"Bot failed to start: {e}")
            sys.exit(1)
    else:
        logger.critical("Bot initialization aborted due to pre-flight check failure.")
        sys.exit(1)
