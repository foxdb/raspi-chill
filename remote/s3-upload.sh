#!/bin/bash

export PATH=~/.local/bin:$PATH

# sync all logs
~/.local/bin/aws s3 sync /home/pi/raspi-chill/logs/ s3://raspi-chill/logs
