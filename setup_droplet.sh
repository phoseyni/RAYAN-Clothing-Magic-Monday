#!/bin/bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv zip
mkdir -p "/root/crypto_bot"
unzip -o "/root/crypto_bot.zip" -d "/root/crypto_bot"
cd "/root/crypto_bot"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cat <<SVC | sudo tee /etc/systemd/system/cryptobot.service
[Unit]
Description=Crypto Bot
After=network.target
[Service]
User=root
WorkingDirectory=/root/crypto_bot
ExecStart=/root/crypto_bot/venv/bin/python bot.py
Restart=always
[Install]
WantedBy=multi-user.target
SVC
sudo systemctl daemon-reload
sudo systemctl enable cryptobot
echo "Setup complete!"
