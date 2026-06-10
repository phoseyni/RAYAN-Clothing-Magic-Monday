# DigitalOcean Clean Installation Guide (Bot v1.1.4)

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

## 3. Configuration (IMPORTANT)
The bot will crash if keys are missing.
```bash
cd /root/crypto_bot
cp .env.template .env
# Edit .env and add your Alpaca and Mailjet keys
```

## 4. Start the Bot
```bash
sudo systemctl start cryptobot
```

## 5. Troubleshooting
If the bot fails to start, check the logs:
`tail -n 50 /root/crypto_bot/bot.log`

**Common Cause**: Missing or incorrect API keys in `.env`. The bot v1.1.4 now performs a "pre-flight check" and will log the specific missing key.

---

## Future Updates
Update your code from your **local computer**:
`./deploy_to_do.sh 165.227.175.240`
