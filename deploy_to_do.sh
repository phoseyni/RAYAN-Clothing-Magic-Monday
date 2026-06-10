#!/bin/bash
# Local deployment script v1.1.4

DROPLET_IP=$1

FILES=("bot.py" "config.py" "exchange_interface.py" "strategy.py" "visualize.py" "email_notifier.py" "requirements.txt" "README.md" "DIGITAL_OCEAN.md" ".env.template" "update_bot.sh" "setup_droplet.sh" "deploy_to_do.sh" "tests/")

echo "Packaging bot v1.1.4..."
rm -f crypto_bot.zip
zip -r crypto_bot.zip "${FILES[@]}"

if [ "$DROPLET_IP" != "LOCAL_SKIP_UPLOAD" ]; then
    echo "Uploading package to $DROPLET_IP..."
    scp crypto_bot.zip root@$DROPLET_IP:/root/

    echo "Triggering remote update..."
    ssh root@$DROPLET_IP "bash /root/crypto_bot/update_bot.sh"
    echo "Deployment finished! Your bot is now updated to v1.1.4."
else
    echo "Package created locally: crypto_bot.zip"
fi
