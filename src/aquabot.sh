#!/usr/bin/bash
#
#   Created on 22th Nov 2020
#   08:11 AM
#   @aquabellus
#

declare -r input=$(eval echo $HOME)/Documents/The-Box/helper/aquabot.pid

while true; do
    if ps -p $(cat $input) | grep -o $(cat $input); then
        sleep 1
    else
        python3 $(eval echo $HOME)/Documents/The-Box/aquabot.py
    fi
    sleep 5
done