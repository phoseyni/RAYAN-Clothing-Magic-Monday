import time
import logging
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

        # 3. Execute trade
        if signal == 'buy':
            self.execute_buy(ohlcv)
        elif signal == 'sell':
            self.execute_sell(ohlcv)
        else:
            logger.info("No action taken. Surviving...")

    def execute_buy(self, ohlcv):
        if self.position == 'long':
            logger.info("Already in a long position.")
            return

        current_price = ohlcv[-1][4]
        order = self.exchange.create_market_order(Config.SYMBOL, 'buy', Config.TRADE_AMOUNT)
        if order:
            logger.info(f"Buy order executed: {order['id']}")
            self.position = 'long'
            self.entry_price = current_price

            # Send Notification
            plot_strategy(ohlcv, []) # Generate chart
            EmailNotifier.send_trade_notification(
                subject=f"TRADE OPENED: Buy {Config.SYMBOL}",
                body=f"Price: {current_price}\nAmount: {Config.TRADE_AMOUNT}\nTime: {time.ctime()}",
                attachment_path="trading_plot.png"
            )

    def execute_sell(self, ohlcv):
        if self.position != 'long':
            logger.info("No long position to close.")
            return

        current_price = ohlcv[-1][4]
        order = self.exchange.create_market_order(Config.SYMBOL, 'sell', Config.TRADE_AMOUNT)
        if order:
            logger.info(f"Sell order executed: {order['id']}")

            # Calculate profit/loss
            pnl_pct = (current_price - self.entry_price) / self.entry_price * 100

            # Send Notification
            plot_strategy(ohlcv, []) # Generate chart
            EmailNotifier.send_trade_notification(
                subject=f"TRADE CLOSED: Sell {Config.SYMBOL}",
                body=f"Price: {current_price}\nPNL: {pnl_pct:.2f}%\nTime: {time.ctime()}",
                attachment_path="trading_plot.png"
            )

            self.position = None
            self.entry_price = None

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
