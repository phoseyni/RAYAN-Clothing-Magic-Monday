#!/bin/bash
BOT_DIR="/root/crypto_bot"
echo "Updating Crypto Bot..."
find "$BOT_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
unzip -o "/root/crypto_bot.zip" -d "$BOT_DIR"
cd "$BOT_DIR"
source venv/bin/activate || (python3 -m venv venv && source venv/bin/activate)
pip install -r requirements.txt
sudo systemctl restart cryptobot
echo "Update complete!"
