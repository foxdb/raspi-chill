import os
import logging
import ConfigParser
from time import sleep
from datetime import datetime
from sensor import read_temperature
from buzzer import alarm, notify_init
from cooler import turn_cooling_off, turn_cooling_on
from db import writeToFile

# TODO: Logging https://docs.python.org/2/howto/logging.html

TARGET_TEMP = 10


def main():
    config = ConfigParser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

    SECONDS_INTERVAL = config.getint('time', 'measure_every')

    logging.basicConfig(filename='regulate.log', level=logging.DEBUG)

    log('one shot cooling has started with target temperature: ' + str(TARGET_TEMP))
    current_temp = read_temperature()
    log('current temperature is: ' + str(current_temp))

    notify_init()

    while current_temp > TARGET_TEMP:
        current_temp = read_temperature()
        print "current temp:", current_temp

        if current_temp > TARGET_TEMP:
            turn_cooling_on()

        if current_temp <= TARGET_TEMP:
            turn_cooling_off()

        writeToFile(get_date(), current_temp)
        sleep(SECONDS_INTERVAL)

    turn_cooling_off()


def get_date():
    return datetime.now().strftime('%Y%m%d_%H-%M-%S')


def log(message):
    logging.info(get_date() + ': ' + message)


main()
