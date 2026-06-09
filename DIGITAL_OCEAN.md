# DigitalOcean Deployment Guide

This guide will help you deploy your autonomous crypto trading bot with email notifications.

## 1. Create a Droplet
- Log in to your DigitalOcean account.
- Click **Create** -> **Droplets**.
- Choose Ubuntu 22.04 LTS and a Basic Shared CPU plan.

## 2. Prepare the Droplet
```bash
ssh root@your_droplet_ip
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv zip
```

## 3. Upload and Unzip
```bash
scp crypto_bot.zip root@your_droplet_ip:/root/
unzip crypto_bot.zip -d crypto_bot
cd crypto_bot
```

## 4. Set Up Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
# Edit .env and add your Alpaca keys AND SMTP credentials
```
*Note: For Gmail, you must use an **App Password**, not your regular password.*

## 5. Background Service
Create `/etc/systemd/system/cryptobot.service`:
```ini
[Unit]
Description=Autonomous Crypto Trading Bot
After=network.target

[Service]
User=root
WorkingDirectory=/root/crypto_bot
ExecStart=/root/crypto_bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable cryptobot
sudo systemctl start cryptobot
```

## 6. Monitor
Status: `sudo systemctl status cryptobot`
Logs: `tail -f bot.log`
