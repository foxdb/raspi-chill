#!/bin/bash

# everything is to debug here, just throwing random cmds without testing

pip install -r requirements.txt
cp config.example.ini config.ini
# make edits to config.ini
chmod +x src/spindel_server.py
chmod +x src/regulate.py
mkdir src/logs

# then "contrab -e" and add:

# */5 * * * * /home/pi/raspi-chill/remote/s3-upload.sh
# @reboot sleep 5 && nohup sudo python3 /home/pi/raspi-chill/src/regulate.py &