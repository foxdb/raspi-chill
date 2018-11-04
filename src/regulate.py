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

    PASSIVE_SECONDS_INTERVAL = config.getint('time', 'passive_cycle_time')
    COOLING_SECONDS_INTERVAL = config.getint('time', 'cooling_cycle_time')
    LOGS_DIRECTORY = config.get('data', 'logs_directory')
    UPPER_LIMIT = config.getint('temperatures', 'maintain_less_than')
    ALARM_LIMIT = config.getint('temperatures', 'alarm_over')

    START_DATE = get_date()

    log_file = raw_input(
        "temperature log file? (Enter generates a new one): ")

    if (log_file):
        TEMPERATURE_LOG_FILE = LOGS_DIRECTORY + '/' + log_file
        REGULATE_LOG_FILE = LOGS_DIRECTORY + '/' + \
            log_file.replace('-temperature.log', '-regulate.log')
        print '- logging temperature to ' + TEMPERATURE_LOG_FILE
        print '- logging events to ' + REGULATE_LOG_FILE
        init_log_file(TEMPERATURE_LOG_FILE)
        logging.basicConfig(filename=REGULATE_LOG_FILE, level=logging.DEBUG)
    else:
        TEMPERATURE_LOG_FILE = LOGS_DIRECTORY + '/' + START_DATE + '-temperature.log'
        REGULATE_LOG_FILE = LOGS_DIRECTORY + '/' + START_DATE + '-regulate.log'
        print '- logging temperature to ' + TEMPERATURE_LOG_FILE
        print '- logging events to ' + REGULATE_LOG_FILE
        init_log_file(TEMPERATURE_LOG_FILE)
        logging.basicConfig(filename=REGULATE_LOG_FILE, level=logging.DEBUG)

    log('- regulation has started with target temperature: ' + str(UPPER_LIMIT))
    log('- current temperature is: ' + str(read_temperature()))

    notify_init()

    alarm_cycles = 0

    while True:
        current_temp = read_temperature()
        writeToFile(TEMPERATURE_LOG_FILE, get_date(), current_temp)

        if current_temp > ALARM_LIMIT:
            alarm()
            alarm_cycles += 1
            log('ALARM - ' + str(alarm_cycles) + ' consecutive cycles')

        if current_temp > UPPER_LIMIT:
            turn_cooling_on()
            sleep(COOLING_SECONDS_INTERVAL)

        if current_temp <= UPPER_LIMIT:
            turn_cooling_off()
            alarm_cycles = 0
            sleep(PASSIVE_SECONDS_INTERVAL)


def get_date():
    return datetime.now().strftime('%Y%m%d_%H-%M-%S')


def log(message):
    print get_date() + ': ' + message
    logging.info(get_date() + ': ' + message)


main()
