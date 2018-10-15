from gpiozero import DigitalOutputDevice
from time import sleep
import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

FAN_GPIO = config.getint('actuators', 'fan_gpio')

fan = DigitalOutputDevice(FAN_GPIO)

# fns: on, off, close
# params: value


def turn_fan_on():
    if fan.value == False:
        fan.on()


def turn_fan_off():
    if fan.value == True:
        fan.off()


def is_fan_on():
    return fan.value
