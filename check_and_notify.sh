#!/usr/bin/env bash

# First check if there are new messages, passing any args (e.g. --force-new for debugging)
# To be able to run this script from any working directory, we get the path to this folder with "dirname $0"
new_msgs=$(python3 $(dirname $0)/scrape.py ${@:1})
if [[ -n "$new_msgs" ]]; then
    # Shows a notification on Ubuntu
    notify-send "New messages! ${new_msgs}"
    xdg-open "https://www.saigaslife.nl"
fi
