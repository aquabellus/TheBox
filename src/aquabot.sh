#!/bin/bash
#
#   Created on 22th Nov 2020
#   08:11 AM
#   @aquabellus
#

declare -r dir=$(eval echo $HOME)/Documents/The-Box

while true; do
    cd $dir
    if ps -p $(cat helper/aquabot.pid) | grep -o $(cat helper/aquabot.pid); then
        sleep 1
    else
        python3 aquabot.py
    fi
    sleep 5
    clear
done