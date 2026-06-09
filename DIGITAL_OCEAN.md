# DigitalOcean Deployment Guide

This guide will help you deploy your autonomous crypto trading bot to a DigitalOcean Droplet.

## 1. Create a Droplet
- Log in to your DigitalOcean account.
- Click **Create** -> **Droplets**.
- **Choose an Image**: Ubuntu 22.04 LTS (or newer).
- **Choose a Plan**: Basic (Shared CPU).
- **Choose a Datacenter Region**: Select one closest to you.
- **Authentication**: SSH keys are recommended.

## 2. Prepare the Droplet
Connect via SSH:
```bash
ssh root@your_droplet_ip
```

Update system and install dependencies:
```bash
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
# Edit .env and add your Alpaca keys using 'nano .env' or 'vi .env'
```

## 5. Background Service
Create a file at `/etc/systemd/system/cryptobot.service` with this content:
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

Enable and start the service:
```bash
sudo systemctl enable cryptobot
sudo systemctl start cryptobot
```

## 6. Monitor
Check status: `sudo systemctl status cryptobot`
View logs: `tail bot.log`
