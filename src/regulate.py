import os
import logging
import ConfigParser
from time import sleep
from datetime import datetime
from sensor import read_temperature
from buzzer import alarm, notify_init
from cooler import turn_cooling_off, turn_cooling_on
from db import writeToFile, init_log_file


def main():
    config = ConfigParser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

    SECONDS_INTERVAL = config.getint('time', 'measure_every')
    LOGS_DIRECTORY = config.get('data', 'logs_directory')
    UPPER_LIMIT = config.getint('temperatures', 'maintain_less_than')
    ALARM_LIMIT = config.getint('temperatures', 'alarm_over')
    CYCLES_BEFORE_ALARM = config.getint('time', 'cycles_before_alarm')

    START_DATE = get_date()

    TEMPERATURE_LOG_FILE = LOGS_DIRECTORY + '/' + START_DATE + '-temperature.log'
    REGULATE_LOG_FILE = LOGS_DIRECTORY + '/' + START_DATE + '-regulate.log'

    init_log_file(TEMPERATURE_LOG_FILE)
    logging.basicConfig(filename=REGULATE_LOG_FILE, level=logging.DEBUG)

    log('regulation has started with target temperature: ' + str(UPPER_LIMIT))
    log('current temperature is: ' + str(read_temperature()))

    notify_init()

    alarm_cycles = 0

    while True:
        current_temp = read_temperature()

        if current_temp > UPPER_LIMIT:
            turn_cooling_on()

        if current_temp <= UPPER_LIMIT:
            turn_cooling_off()
            alarm_cycles = 0

        if current_temp > ALARM_LIMIT:
            alarm()
            alarm_cycles += 1
            log('ALARM - ' + str(alarm_cycles) + ' consecutive cycles')

        if alarm_cycles % CYCLES_BEFORE_ALARM == 0 and alarm_cycles != 0:
            print "--> sms"
            log('sent alarm notification')

        writeToFile(TEMPERATURE_LOG_FILE, get_date(), current_temp)
        sleep(SECONDS_INTERVAL)


def get_date():
    return datetime.now().strftime('%Y%m%d_%H-%M-%S')


def log(message):
    print get_date() + ': ' + message
    logging.info(get_date() + ': ' + message)


main()
