# DigitalOcean One-Command Deployment Guide

I have automated most of the installation. Here is how to reinstall or set up the bot on your Droplet (**165.227.175.240**).

## 1. Upload the zip
From your **local computer**, upload the zip file:
```bash
scp crypto_bot.zip root@165.227.175.240:/root/
```

## 2. Run the Setup Script
Connect to your Droplet via SSH and run the setup script:
```bash
ssh root@165.227.175.240
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
Once installed, you can update the bot from your **local computer** with one command:
```bash
./deploy_to_do.sh 165.227.175.240
```

## Monitoring
- Status: `sudo systemctl status cryptobot`
- Logs: `tail -f /root/crypto_bot/bot.log`
