from time import sleep
from sensor import read_temperature
from buzzer import notify_init
from cooler import turn_cooling_off, turn_cooling_on

print """raspi-chill - hardware tests
      - temperature sensor reading
      - buzzer
      - cooling device"""

raw_input('Press Enter (temperature sensor)')

print read_temperature()

raw_input('Press Enter (buzzer)')

notify_init()

raw_input('Press Enter (cooler 5 seconds)')

turn_cooling_on()
sleep(5)
turn_cooling_off()

print "No more tests for now!"
