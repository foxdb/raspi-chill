# raspi-chill

## Setup

- `./install.sh`

## Usage

- **Continous** - monitor and maintain temperature

`nohup sudo ./src/regulate.py --name NAME &`

Hot updates of `config.ini` are supported. Example usecase: change the regulation temperature, cycle time, ...

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

### Sensor

- Digital temperature sensor: DS18B20

### During prototyping

- Breadboard
- Jumper cables
- Another thermometer for calibration
