# raspi-chill

## Usage

- **Continous** - monitor and maintain temperature

`python src/core.py`

- **One shot** - take the environment to a target temperature

`python src/refresh.py`

## Hardware (box)

> FreeCAD design and panels measurements in `cad/iceBox.fcstd`

## Hardware (electronics)

### Misc

- 12 VDC 80 mm fan
- 12 VDC relay
- Raspberry Pi 3
- Relay module

### Power supplies

- 12 V at 400 mA power supply
- 5 V at 1A power supply

> Even better: work with one 12 VDC only (1-2A) and a regulator for the Raspberry.

### Sensor

- Digital temperature sensor: DS18B20

### During prototyping

- Breadboard
- Jumper cables
- Another thermometer for calibration
