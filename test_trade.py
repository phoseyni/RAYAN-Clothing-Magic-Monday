import logging
import sys
from exchange_interface import ExchangeInterface
from config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_test():
    print(f"--- Alpaca Test Trade Utility v{Config.VERSION} ---")
    try:
        interface = ExchangeInterface()
        symbol = Config.SYMBOL
        amount = 0.001 # Minimum for BTC/USD on Alpaca is ~10 USD worth

        print(f"Checking ticker for {symbol}...")
        ticker = interface.fetch_ticker(symbol)
        if ticker:
            price = ticker['last']
            print(f"Current Price: {price}")

            print(f"Placing a small BUY order (0.001 {symbol})...")
            order = interface.create_market_order(symbol, 'buy', amount)

            if order:
                print("SUCCESS: Buy order placed.")
                print(f"Order ID: {order['id']}")
                print(f"Status: {order['status']}")

                # Immediate sell to close the test position (survive little by little!)
                print(f"Closing position with a SELL order...")
                sell_order = interface.create_market_order(symbol, 'sell', amount)
                if sell_order:
                    print("SUCCESS: Position closed.")
                else:
                    print("WARNING: Manual action might be needed to close the position.")
            else:
                print("FAILED: Order could not be placed. Check your keys and balance.")
        else:
            print("FAILED: Could not fetch market data.")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Check if .env exists
    import os
    if not os.path.exists('.env'):
        print("ERROR: .env file not found. Please create it first.")
        sys.exit(1)
    run_test()
