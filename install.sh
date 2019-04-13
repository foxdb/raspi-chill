#!/bin/bash

# everything is to debug here, just throwing random cmds without testing
pip install -r requirements.txt
cp config.example.ini config.ini
chmod +x src/spindel_server.py
chmod +x src/regulate.py
mkdir src/logs