from gpiozero import DigitalOutputDevice
from time import sleep
import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

COOLING_GPIO = config.getint('actuators', 'cooling_gpio')

cooling = DigitalOutputDevice(COOLING_GPIO)

# fns: on, off, close
# params: value

# relay wiring is inverted


def turn_cooling_on():
    #     if cooling.value == True:
    cooling.off()


def turn_cooling_off():
    #     if cooling.value == False:
    cooling.on()


def is_cooling_on():
    return cooling.value


print 'turning on'
turn_cooling_off()

sleep(10)

print 'turning off'
turn_cooling_on()
