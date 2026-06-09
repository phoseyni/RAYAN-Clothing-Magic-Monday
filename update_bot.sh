#!/bin/bash
# Server-side update script

BOT_DIR="/root/crypto_bot"
ZIP_FILE="/root/crypto_bot.zip"

echo "Updating Crypto Bot..."

# Unzip new version, overwriting existing files
unzip -o "$ZIP_FILE" -d "$BOT_DIR"

cd "$BOT_DIR"

# Ensure venv is up to date
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Warning: venv not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Restart the service
echo "Restarting cryptobot service..."
sudo systemctl restart cryptobot

echo "Update complete! Status:"
sudo systemctl status cryptobot --no-pager
