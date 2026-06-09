# Advanced Autonomous Crypto Trading Bot

An autonomous trading bot with multi-strategy support and risk management.

## Features
- **Multiple Strategies**:
  - **EMA**: Exponential Moving Average crossover for trending markets.
  - **MEAN_REVERSION**: RSI-based oversold/overbought signals.
  - **GRID**: Grid trading for sideways movements (Simplified implementation).
  - **DCA**: Interval-based Dollar-Cost Averaging.
- **Risk Management**: Bolder Stop Loss (5%) and Take Profit (10%) for paper trading.
- **Visualisation**: Generates SMA/EMA charts for every trade.
- **Notifications**: Automated email alerts via Mailjet with chart attachments.

## Configuration
Set \`STRATEGY_MODE\` in your \`.env\` file to one of: \`EMA\`, \`MEAN_REVERSION\`, \`GRID\`, \`DCA\`.

## Installation & Deployment
See [DIGITAL_OCEAN.md](DIGITAL_OCEAN.md) for automated deployment instructions.
