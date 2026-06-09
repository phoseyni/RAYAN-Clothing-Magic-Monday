#!/bin/bash
# Local deployment script v1.1.3
DROPLET_IP=$1
if [ -z "$DROPLET_IP" ]; then
    echo "Usage: ./deploy_to_do.sh <DROPLET_IP>"
else
    echo "Packaging bot v1.1.3..."
    rm -f crypto_bot.zip
    # Directly naming files to avoid globbing issues
    zip -r crypto_bot.zip bot.py config.py exchange_interface.py strategy.py visualize.py email_notifier.py requirements.txt README.md DIGITAL_OCEAN.md .env.template update_bot.sh setup_droplet.sh deploy_to_do.sh tests/
    if [ ! -f "crypto_bot.zip" ]; then
        echo "Error: Failed to create crypto_bot.zip. File list might be wrong."
    else
        echo "Uploading package to $DROPLET_IP..."
        scp crypto_bot.zip root@$DROPLET_IP:/root/
        echo "Triggering remote update..."
        ssh root@$DROPLET_IP "bash /root/crypto_bot/update_bot.sh"
        echo "Deployment finished! Your bot is now updated to v1.1.3."
    fi
fi
