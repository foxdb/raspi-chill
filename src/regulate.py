#!/usr/bin/env python3

import os
import configparser
import threading
from time import sleep
from sensor import read_temperature
from buzzer import alarm, notify_init, is_buzzer_on, turn_buzzer_off
from cooler import turn_cooling_off, turn_cooling_on, is_cooling_on
from db import Logger, get_date
from spindel_server import spindel_server
from tilt_read import tilt_read


def main(logger, config_file):
    config = get_config(config_file)
    init_temp = read_temperature()

    notify_init()

    logger.info('raspi-chill has started!')
    logger.info('[ REGULATION ]')
    logger.info('- initial ext temperature: %s' % init_temp)
    logger.info('- target ext temperature:  %s' % config.get('UPPER_LIMIT'))
    logger.info('- regulation enabled: %s' % config.get('REGULATION_ENABLED'))
    logger.info('- cooling cycle time: %s' %
                config.get('COOLING_SECONDS_INTERVAL'))
    logger.info('- passive cycle time: %s' %
                config.get('PASSIVE_SECONDS_INTERVAL'))
    logger.info('[ LOGS ]')
    logger.info('- int temperature log: %s' %
                (logger.INTERNAL_TEMPERATURE_LOG_FILE))
    logger.info('- ext temperature log: %s' %
                (logger.EXTERNAL_TEMPERATURE_LOG_FILE))
    logger.info('- gravity log: %s' % (logger.GRAVITY_LOG_FILE))
    logger.info('- events log: %s' % (logger.EVENTS_LOG_FILE))

    alarm_cycles = 0

    while True:
        # refresh config
        config = get_config(config_file)

        current_temp = read_temperature()
        logger.writeExternalTemperature(current_temp)

        if config.get('REGULATION_ENABLED'):
            if current_temp > config.get('ALARM_LIMIT'):
                alarm()
                alarm_cycles += 1
                logger.info('ALARM - %s consecutive cycles' % alarm_cycles)

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


def get_config(config_file):
    config_input = configparser.ConfigParser()
    config_input.read(config_file)

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


if __name__ == "__main__":
    print('parsing config...')
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='project name, included in log files')
    args = parser.parse_args()

    if args.name == None:
        logger = Logger(get_date())
    else:
        logger = Logger(args.name)

    config_file = os.path.dirname(
        os.path.realpath(__file__)) + "/config.ini"

    print('initializing regulation_thread...')
    regulation_thread = threading.Thread(
        target=main, args=(logger, config_file,))

    print('initializing http_thread...')
    http_thread = threading.Thread(target=spindel_server, args=(logger, config_file, 85))

    print('initializing tilt_thread...')
    tilt_thread = threading.Thread(target=tilt_read, args=(logger, config_file,))

    print('starting tilt_thread...')
    tilt_thread.start()
    print('starting regulation_thread...')
    regulation_thread.start()
    print('starting http_thread...')
    http_thread.start()

    #  TODO handle KeyboardInterrupt, handle process kill
