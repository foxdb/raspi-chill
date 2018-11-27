import os
import logging
import ConfigParser
from time import sleep
from datetime import datetime
from sensor import read_temperature
from buzzer import alarm, notify_init, is_buzzer_on, turn_buzzer_off
from cooler import turn_cooling_off, turn_cooling_on, is_cooling_on
from db import writeToFile, init_log_file

import sys


def main():
    config = get_config()
    START_DATE = get_date()
    init_temp = read_temperature()

    # allow user to give temperature log file through cmd args
    if (sys.argv[1]):
        TEMPERATURE_LOG_FILE = config.get('LOGS_DIRECTORY') + '/' + sys.argv[1]
        EVENTS_LOG_FILE = config.get('LOGS_DIRECTORY') + '/' + \
            sys.argv[1].replace('-temperature.log', '-regulate.log')

        init_log_file(TEMPERATURE_LOG_FILE)
        logging.basicConfig(filename=EVENTS_LOG_FILE, level=logging.DEBUG)

    else:
        TEMPERATURE_LOG_FILE = config.get(
            'LOGS_DIRECTORY') + '/' + START_DATE + '-temperature.log'
        EVENTS_LOG_FILE = config.get(
            'LOGS_DIRECTORY') + '/' + START_DATE + '-regulate.log'

        init_log_file(TEMPERATURE_LOG_FILE)
        logging.basicConfig(filename=EVENTS_LOG_FILE, level=logging.DEBUG)

    notify_init()

    log('raspi-chill has started!')
    log('[ REGULATION ]')
    log('- current temperature: ' + str(init_temp))
    log('- target temperature: ' + str(config.get('UPPER_LIMIT')))
    log('- regulation enabled: ' + str(config.get('REGULATION_ENABLED')))
    log('- cooling cycle time: ' + str(config.get('COOLING_SECONDS_INTERVAL')))
    log('- passive cycle time: ' + str(config.get('PASSIVE_SECONDS_INTERVAL')))
    log('[ LOGS ]')
    log('- temperature log file: ' + str(TEMPERATURE_LOG_FILE))
    log('- events log file: ' + str(EVENTS_LOG_FILE))

    alarm_cycles = 0

    while True:
        # refresh config
        config = get_config()

        current_temp = read_temperature()
        writeToFile(TEMPERATURE_LOG_FILE, get_date(), current_temp)

        if config.get('REGULATION_ENABLED'):
            if current_temp > config.get('ALARM_LIMIT'):
                alarm()
                alarm_cycles += 1
                log('ALARM - ' + str(alarm_cycles) + ' consecutive cycles')

            if current_temp > config.get('UPPER_LIMIT'):
                turn_cooling_on()
                sleep(config.get('COOLING_SECONDS_INTERVAL'))

            if current_temp <= config.get('UPPER_LIMIT'):
                turn_cooling_off()
                alarm_cycles = 0
                sleep(config.get('PASSIVE_SECONDS_INTERVAL'))

        else:
            if is_cooling_on():
                turn_cooling_off()
            sleep(config.get('PASSIVE_SECONDS_INTERVAL'))


def get_date():
    return datetime.now().strftime('%Y%m%d_%H-%M-%S')


def log(message):
    print get_date() + ': ' + message
    logging.info(get_date() + ': ' + message)


def get_config():
    config_input = ConfigParser.ConfigParser()
    config_input.read(os.path.dirname(
        os.path.realpath(__file__)) + "/config.ini")

    config = dict()

    config['PASSIVE_SECONDS_INTERVAL'] = config_input.getint(
        'time', 'passive_cycle_time')
    config['COOLING_SECONDS_INTERVAL'] = config_input.getint(
        'time', 'cooling_cycle_time')
    config['LOGS_DIRECTORY'] = config_input.get('data', 'logs_directory')
    config['UPPER_LIMIT'] = config_input.getint(
        'temperatures', 'maintain_less_than')
    config['ALARM_LIMIT'] = config_input.getint('temperatures', 'alarm_over')
    config['REGULATION_ENABLED'] = config_input.getboolean(
        'temperatures', 'regulation_enabled')

    return config


main()
