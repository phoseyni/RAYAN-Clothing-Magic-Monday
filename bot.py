import time
import logging
from config import Config
from exchange_interface import ExchangeInterface
from strategy import Strategy
from visualize import plot_strategy
from email_notifier import EmailNotifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self):
        self.exchange = ExchangeInterface()
        self.entry_price = None
        self.position = None
        self.last_dca_time = 0

    def run(self):
        logger.info(f"Starting trading bot v{Config.VERSION} on {Config.EXCHANGE_ID} in {Config.STRATEGY_MODE} mode...")
        while True:
            try:
                self.tick(); time.sleep(60)
            except KeyboardInterrupt: break
            except Exception as e: logger.error(f"Loop error: {e}"); time.sleep(30)

    def tick(self):
        ohlcv = self.exchange.fetch_ohlcv(Config.SYMBOL, Config.TIMEFRAME)
        if not ohlcv: return
        if Config.STRATEGY_MODE == 'DCA': self.handle_dca(); return
        df = Strategy.calculate_indicators(ohlcv)
        signal = Strategy.get_signal(df, self.entry_price)
        if signal == 'buy': self.execute_buy(ohlcv)
        elif signal == 'sell': self.execute_sell(ohlcv)

    def handle_dca(self):
        if time.time() - self.last_dca_time >= (Config.DCA_INTERVAL_MINUTES * 60):
            order = self.exchange.create_market_order(Config.SYMBOL, 'buy', Config.DCA_AMOUNT)
            if order:
                self.last_dca_time = time.time()
                EmailNotifier.send_trade_notification(f"DCA BUY: {Config.SYMBOL}", f"Amt: {Config.DCA_AMOUNT}\nVer: {Config.VERSION}")

    def execute_buy(self, ohlcv):
        if self.position == 'long': return
        order = self.exchange.create_market_order(Config.SYMBOL, 'buy', Config.TRADE_AMOUNT)
        if order:
            self.position, self.entry_price = 'long', ohlcv[-1][4]
            plot_strategy(ohlcv, [])
            EmailNotifier.send_trade_notification(f"OPENED: Buy {Config.SYMBOL}", f"Price: {self.entry_price}\nVer: {Config.VERSION}", "trading_plot.png")

    def execute_sell(self, ohlcv):
        if self.position != 'long': return
        order = self.exchange.create_market_order(Config.SYMBOL, 'sell', Config.TRADE_AMOUNT)
        if order:
            pnl = (ohlcv[-1][4] - self.entry_price) / self.entry_price * 100
            plot_strategy(ohlcv, [])
            EmailNotifier.send_trade_notification(f"CLOSED: Sell {Config.SYMBOL}", f"Price: {ohlcv[-1][4]}\nPNL: {pnl:.2f}%\nVer: {Config.VERSION}", "trading_plot.png")
            self.position = self.entry_price = None

if __name__ == "__main__":
    TradingBot().run()
