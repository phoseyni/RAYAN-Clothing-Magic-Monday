# Autonomous Crypto Trading Bot

An autonomous trading bot designed to work with European-compatible exchanges (default: Kraken) using the CCXT library.

## Features
- Autonomous execution loop
- SMA Crossover trading strategy
- Integrated with CCXT for broad exchange support
- Secure configuration via environment variables
- Detailed logging

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables in a `.env` file:
   ```env
   EXCHANGE_ID=kraken
   EXCHANGE_API_KEY=your_api_key
   EXCHANGE_SECRET=your_secret
   TRADING_SYMBOL=BTC/EUR
   TIMEFRAME=1h
   SMA_FAST=10
   SMA_SLOW=30
   TRADE_AMOUNT=0.001
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

## Testing
Run tests using:
```bash
python -m pytest
```
