#!/bin/bash
#
#   Created on 22th Nov 2020
#   08:11 AM
#   @aquabellus
#

while true; do
    cd /home/$(whoami)/Documents/The-Box/
    if ps -p $(cat ./helper/aquabot.pid) | grep -o $(cat ./helper/aquabot.pid); then
        sleep 5
    else
        lxterminal -e python3 ./aquabot.py
        sleep 5
    fi
    clear
done