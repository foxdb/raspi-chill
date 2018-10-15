import os
import glob
import time
import ConfigParser

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

device_directory = config.get('sensors', 'temp_device_folder')
device_folder = glob.glob(device_directory + '28*')[0]
device_file = device_folder + '/' + \
    config.get('sensors', 'temp_device_filename')


def read_temperature_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# example reading
# 77 01 4b 46 7f ff 0c 10 90 : crc=90 YES
# 77 01 4b 46 7f ff 0c 10 90 t=23437


MAX_TRIES = 10
TEMP_IDENTIFIER = 't='


def read_temperature():
    attempt = 0

    lines = read_temperature_raw()

    while 'YES' not in lines[0] and attempt < MAX_TRIES:
        attempt += 1
        time.sleep(0.2)
        lines = read_temperature_raw()

    position = lines[1].find(TEMP_IDENTIFIER)
    if position != -1:
        temp_string = lines[1][position+len(TEMP_IDENTIFIER):]
        temp_c = float(temp_string) / 1000.0
        return temp_c
