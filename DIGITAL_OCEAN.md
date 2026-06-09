# DigitalOcean Clean Installation Guide (Bot v1.1.3)

Follow these steps to set up your bot on a fresh Droplet (165.227.175.240).

## 1. Upload from your Local Computer
```bash
scp crypto_bot.zip root@165.227.175.240:/root/
```

## 2. Automated System Setup
SSH into the Droplet and run the setup script:
```bash
ssh root@165.227.175.240
unzip crypto_bot.zip setup_droplet.sh
bash setup_droplet.sh
```
*This installs Python, sets up the virtual environment, and creates the background service.*

## 3. Configuration
```bash
cd /root/crypto_bot
cp .env.template .env
# Use 'nano .env' to add your Alpaca and Mailjet keys
```

## 4. Start the Bot
```bash
sudo systemctl start cryptobot
```

## 5. Monitoring
- **Status**: `sudo systemctl status cryptobot`
- **Live Logs**: `tail -f /root/crypto_bot/bot.log`

---

## Future Updates
To update your code in the future, just run this from your **local computer**:
```bash
./deploy_to_do.sh 165.227.175.240
```
