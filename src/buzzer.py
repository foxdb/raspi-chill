#  buzz on start
#  buzz on alarm

from gpiozero import Buzzer
from time import sleep
import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

BUZZER_GPIO = config.getint('actuators', 'buzzer_gpio')

buzzer = Buzzer(BUZZER_GPIO)

# fns: on, off, close
# params: value

# relay wiring is inverted


def is_buzzer_on():
    return buzzer.value


def notify_init():
    buzzer.on()
    sleep(0.10)
    buzzer.off()
    sleep(0.10)
    buzzer.on()
    sleep(0.10)
    buzzer.off()


def alarm():
    buzzer.on()
    sleep(0.5)
    buzzer.off()
