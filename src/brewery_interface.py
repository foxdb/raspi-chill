#!/usr/bin/env python3
"""
Display data on LCD, allow for on-demand measurement and display on LCD

start standalone with "sudo python3 brewery_interface.py"

"""

from db import Logger
from time import sleep
import os
import lcd
import sys
import keyboard
from tilt_read import get_tilt_readings 

TILT_ACQUISITION_TIME_S = 10

# TODO: keyboard event handler to avoid repeating code - see while True:

def brewery_interface(logger, config_file):
    print('Starting brewery interface...')

    init()

    while True:
        event = keyboard.read_event()
        
        if event.event_type == keyboard.KEY_DOWN and event.name == 'space':
            print('space was pressed')

        if event.event_type == keyboard.KEY_DOWN and event.name == 't':
            lcd.write('Tilt acquisition', 'in progress...')

            # TODO: error handling
            print('t pressed, doing a reading of tilts')
            readings = get_tilt_readings(TILT_ACQUISITION_TIME_S)
            print('got readings', readings)

            for reading in readings.values():
                gravity = reading['minor']
                temperature = round((reading['major'] - 32) * 5 / 9, 1)
                color = reading['color']

                lcd.write("{} tilt".format(color), "SG={}, T={}".format(gravity, temperature))
                sleep(5)

            lcd.clear()
            lcd.turn_backlight_off()

        if event.event_type == keyboard.KEY_DOWN and event.name == 'o':
            lcd.write('q: quit program', 'o: show options')
            sleep(4)
            lcd.write('t: read tilts', '')
            sleep(4)
            lcd.clear()
            lcd.turn_backlight_off()

        if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
            # TODO: should exit only if the program is launched by itself
            # i.e. not when started as a thread by main program
            lcd.write('good bye', 'hold my beer')
            sleep(2)
            exit()

def init():
    lcd.write('Your wishes are', 'my command')
    sleep(2)
    lcd.clear()
    lcd.turn_backlight_off()

def exit():
    lcd.turn_off()
    sys.exit()

# run interface on its own, useful for debugging
if __name__ == "__main__":
    try:
        logger = Logger('test')
        config_file = os.path.dirname(
            os.path.realpath(__file__)) + "/config.ini"
        
        brewery_interface(logger, config_file)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            exit()
        except SystemExit:
            os._exit()
