#!/usr/bin/env python3

from tilt_read import get_tilt_readings

input('Press Enter (tilt read)')

readings = get_tilt_readings(10)

print(readings)

for reading in readings.values():
    gravity = reading['minor']
    temperature = round((reading['major'] - 32) * 5 / 9, 1)
    color = reading['color']

    print("{} tilt".format(color))
    print("SG={}, T={}".format(gravity, temperature))
