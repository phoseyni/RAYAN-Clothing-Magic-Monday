#!/bin/bash
# Server-side initial setup script

echo "Initializing system for Crypto Bot..."

# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv zip

# Create bot directory if it doesn't exist
BOT_DIR="/root/crypto_bot"
mkdir -p "$BOT_DIR"

# Extract
echo "Extracting bot files..."
unzip -o "/root/crypto_bot.zip" -d "$BOT_DIR"

cd "$BOT_DIR"

# Set up virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
echo "Creating systemd service..."
cat <<SVC | sudo tee /etc/systemd/system/cryptobot.service
[Unit]
Description=Autonomous Crypto Trading Bot
After=network.target

[Service]
User=root
WorkingDirectory=$BOT_DIR
ExecStart=$BOT_DIR/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
SVC

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable cryptobot

echo "Setup complete!"
echo "Next steps:"
echo "1. Run 'cp $BOT_DIR/.env.template $BOT_DIR/.env'"
echo "2. Edit $BOT_DIR/.env with your keys"
echo "3. Run 'sudo systemctl start cryptobot'"
