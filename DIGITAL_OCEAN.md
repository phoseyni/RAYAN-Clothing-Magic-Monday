# DigitalOcean One-Command Deployment Guide

I have automated most of the installation. Here is how to reinstall or set up the bot from scratch.

## 1. Upload the zip
From your **local computer**, upload the zip file to your root directory:
```bash
scp crypto_bot.zip root@your_droplet_ip:/root/
```

## 2. Run the Setup Script
Connect to your Droplet via SSH and run the setup script directly from the zip:
```bash
ssh root@your_droplet_ip
unzip crypto_bot.zip setup_droplet.sh
bash setup_droplet.sh
```
*This will install Python, set up the virtual environment, and create the background service.*

## 3. Configure and Start
Now just add your keys and start the bot:
```bash
cd /root/crypto_bot
cp .env.template .env
# Edit .env with your keys using 'nano .env'
sudo systemctl start cryptobot
```

---

## Future Updates (Easier)
Once the bot is installed, you can update it in one go from your **local computer**:
```bash
./deploy_to_do.sh your_droplet_ip
```
This will automatically package, upload, and restart the bot for you.

## Monitoring
- Status: `sudo systemctl status cryptobot`
- Logs: `tail -f /root/crypto_bot/bot.log`
