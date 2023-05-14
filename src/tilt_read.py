#!/usr/bin/env python3

import sys
import asyncio
import argparse
import re
import time
import json
import configparser
import requests
import os
from db import Logger
import aioblescan as aiobs
from aioblescan.plugins import Tilt

BLE_DEVICE = 0

red = 'a495bb10c5b14b44b5121370f02d74de'
green = 'a495bb20c5b14b44b5121370f02d74de'
black = 'a495bb30c5b14b44b5121370f02d74de'
purple = 'a495bb40c5b14b44b5121370f02d74de'
orange = 'a495bb50c5b14b44b5121370f02d74de'
blue = 'a495bb60c5b14b44b5121370f02d74de'
yellow = 'a495bb70c5b14b44b5121370f02d74de'
pink = 'a495bb80c5b14b44b5121370f02d74de'

OPEN_READ_TIME_S = 10
READ_INTERVAL_S = 3600

colorDict = {
    'a495bb10c5b14b44b5121370f02d74de': 'red',
    'a495bb20c5b14b44b5121370f02d74de': 'green',
    'a495bb30c5b14b44b5121370f02d74de': 'black',
    'a495bb40c5b14b44b5121370f02d74de': 'purple',
    'a495bb50c5b14b44b5121370f02d74de': 'orange',
    'a495bb60c5b14b44b5121370f02d74de': 'blue',
    'a495bb70c5b14b44b5121370f02d74de': 'yellow',
    'a495bb80c5b14b44b5121370f02d74de': 'pink',
}


def get_tilt_color(uuid):
    return colorDict[uuid]


def get_tilt_readings(open_read_time):

    readings = {}

    def my_process(data):
        ev = aiobs.HCI_Event()
        xx = ev.decode(data)
        xx = Tilt().decode(ev)
        if xx:
            # debug only, otherwise noisy
            # print("{}".format(xx))
            parsedData = json.loads(xx)
            color = get_tilt_color(parsedData['uuid'])
            # extra protection, if no color: that measured thing wasn't a tilt!
            if color:
                readings[parsedData['uuid']] = {'rssi': parsedData['rssi'], 'tx_power': parsedData['tx_power'], 'mac': parsedData['mac'],
                                                'major': parsedData['major'], 'minor': parsedData['minor'], 'uuid': parsedData['uuid'], 'color': color}

    # whoever reads that event_loop voodoo, please don't judge me too hard
    asyncio.set_event_loop(asyncio.new_event_loop())
    event_loop = asyncio.get_event_loop()

    # First create and configure a raw socket
    mysocket = aiobs.create_bt_socket(BLE_DEVICE)

    # create a connection with the raw socket
    # This used to work but now requires a STREAM socket.
    # fac=event_loop.create_connection(aiobs.BLEScanRequester,sock=mysocket)
    # Thanks to martensjacobs for this fix
    fac = event_loop._create_connection_transport(
        mysocket, aiobs.BLEScanRequester, None, None)
    # Start it
    conn, btctrl = event_loop.run_until_complete(fac)
    # Attach your processing
    btctrl.process = my_process

    # print('Starting acquisition for ' + str(open_read_time) + ' s')

    btctrl.send_scan_request()

    async def wait_read_time(future):
        await asyncio.sleep(open_read_time)
        future.set_result('Open read time finished!')

    def got_result(future):
        event_loop.stop()

    future = asyncio.Future()
    asyncio.ensure_future(wait_read_time(future))
    future.add_done_callback(got_result)

    try:
        event_loop.run_forever()
    finally:
       # stop: close event loop
        # print('Stopping acquisition')
        btctrl.stop_scan_request()
        command = aiobs.HCI_Cmd_LE_Advertise(enable=False)
        btctrl.send_command(command)
        conn.close()
        event_loop.close()
        return readings


def get_config(logger, config_file):
    logger.info('Reading config file: ' + str(config_file))
    config_input = configparser.ConfigParser()
    config_input.read(config_file)

    config = dict()

    config['PUSH_ENDPOINT'] = config_input.get(
        'holdmybeer', 'tilt_collection_endpoint')
    config['PUSH_API_KEY'] = config_input.get('holdmybeer', 'apikey')
    config['TILT_COLLECTION_ENABLED'] = config_input.getboolean('holdmybeer', 'tilt_collection_enabled')

    return config


def post_data(url, apikey, body):
    headers = {'content-type': 'application/json', 'x-api-key': apikey}
    requests.post(url, data=json.dumps(body), headers=headers)


def get_and_push_tilt_readings_once(logger, target_endpoint, target_apikey):
    readings = get_tilt_readings(OPEN_READ_TIME_S)
    logger.info('Got readings: ' + str(readings))
    try:
        logger.info('Pushing readings to ' + target_endpoint)
        post_data(target_endpoint, target_apikey, readings)
    except Exception as e:
        logger.info('Failed while posting data to remote server')
        logger.info(str(e))


def tilt_read(logger, config_file):
    logger.info('starting tilt_read')
    logger.info('tilt_read: will get and push tilt readings every ' +
          str(READ_INTERVAL_S) + ' seconds with ' + str(OPEN_READ_TIME_S) + ' seconds acquisition windows.')
    while True:
        config = get_config(logger, config_file)
        target_endpoint = config.get('PUSH_ENDPOINT')
        target_apikey = config.get('PUSH_API_KEY')
        tilt_collection_enabled = config.get('TILT_COLLECTION_ENABLED')

        if tilt_collection_enabled:
            logger.info('tilt_collection_enabled is true, collecting a reading...')
            get_and_push_tilt_readings_once(logger, target_endpoint, target_apikey)
        else:
            logger.info('skipped tilt collection because tilt_collection_enabled is not true')
        time.sleep(READ_INTERVAL_S)


if __name__ == "__main__":
    logger = Logger('test')
    config_file = os.path.dirname(
        os.path.realpath(__file__)) + "/config.ini"
    tilt_read(logger, config_file)
