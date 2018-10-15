import os
import ConfigParser
from time import sleep
from sensor import read_temperature

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

SECONDS_INTERVAL = config.getint('time', 'measure_every')
UPPER_LIMIT = config.getint('temperatures', 'maintain_less_than')
ALARM_LIMIT = config.getint('temperatures', 'alarm_over')
CYCLES_BEFORE_ALARM = config.getint('time', 'cycles_before_alarm')
SLACK = config.getfloat('temperatures', 'slack')

alarm_cycles = 0

while True:
    current_temp = read_temperature()
    print "current temp:", current_temp

    if current_temp > UPPER_LIMIT:
        print "fan on"

    if current_temp <= UPPER_LIMIT:
        print "fan off"

        alarm_cycles = 0

    if current_temp > ALARM_LIMIT:
        alarm_cycles += 1
        # print "THAT'S TOO MUCH BOI, I AM TRIGGERING THE ALARM"

    if alarm_cycles % CYCLES_BEFORE_ALARM == 0:
        print "--> sms"

    if alarm_cycles >= CYCLES_BEFORE_ALARM:
        print "BUZZZZ"

    sleep(SECONDS_INTERVAL)
