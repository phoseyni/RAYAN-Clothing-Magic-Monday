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
        self.last_dca_time = 0
        self.grid_levels = []

    def run(self):
        logger.info(f"Starting trading bot on {Config.EXCHANGE_ID} in {Config.STRATEGY_MODE} mode...")
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

        current_price = ohlcv[-1][4]

        # 2. Strategy Specific Execution
        if Config.STRATEGY_MODE == 'DCA':
            self.handle_dca()
            return

        if Config.STRATEGY_MODE == 'GRID':
            self.handle_grid(current_price)
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
                    body=f"Amount: {Config.DCA_AMOUNT}\nTime: {time.ctime()}"
                )

    def handle_grid(self, current_price):
        if not self.grid_levels:
            self.grid_levels = Strategy.get_grid_levels(current_price)
            logger.info(f"Initialized Grid Levels: {self.grid_levels}")
            return

        # Simple Grid logic: Buy if price drops to a level, Sell if it rises to next
        # (This is a simplified implementation for paper trading boldness)
        # In a real bot, we'd track each level's status
        pass

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
                body=f"Price: {current_price}\nTime: {time.ctime()}",
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
                body=f"Price: {current_price}\nPNL: {pnl_pct:.2f}%\nTime: {time.ctime()}",
                attachment_path="trading_plot.png"
            )

            self.position = None
            self.entry_price = None

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
