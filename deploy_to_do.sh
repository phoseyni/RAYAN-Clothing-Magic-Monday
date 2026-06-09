#!/bin/bash
# Local deployment script

DROPLET_IP=$1

echo "Packaging bot..."
rm -f crypto_bot.zip
zip -r crypto_bot.zip bot.py config.py exchange_interface.py strategy.py visualize.py email_notifier.py requirements.txt README.md DIGITAL_OCEAN.md .env.template update_bot.sh tests/

echo "Uploading package to $DROPLET_IP..."
scp crypto_bot.zip root@$DROPLET_IP:/root/

echo "Triggering remote update..."
ssh root@$DROPLET_IP "bash /root/crypto_bot/update_bot.sh"

echo "Deployment finished!"
