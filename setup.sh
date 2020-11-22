#!/usr/bin/bash
#
#   Created on 22th Nov 2020
#   08:11 AM
#   @aquabellus
#

sudo cp ./src/aquabot.service /etc/systemd/system/
sudo cp ./src/aquabot.sh /usr/sbin/
sudo chmod +x /usr/sbin/aquabot.sh
systemctl daemon-reload
systemctl enable aquabot.service
systemctl start aquabot.service

echo "Service is started !!!"