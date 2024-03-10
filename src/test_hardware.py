#!/usr/bin/env python3

from time import sleep
from sensor import read_temperature
from buzzer import notify_init
from cooler import turn_cooling_off, turn_cooling_on
from tilt_read import get_tilt_readings

print("""raspi-chill - hardware tests
      - tilt acquisition
      - temperature sensor reading
      - buzzer
      - cooling device""")

input('Press Enter (tilt read)')

readings = get_tilt_readings(10)
print(readings)

input('Press Enter (temperature sensor)')

print(read_temperature())

input('Press Enter (buzzer)')

notify_init()

input('Press Enter (cooler 5 seconds)')

turn_cooling_on()
sleep(5)
turn_cooling_off()

print("No more tests for now!")
