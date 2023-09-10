# raspi-chill

Raspi-chill on Raspberry Pi:

- Accepts data sent via HTTP from iSpindels (wifi)
- Gathers data from nearby Tilts (bluetooth)
- Forwards data to the [Hold My Beer](http://hold-my-beer.smitchdigital.com) platform

Previously, it was also turning a fan on/off depending on measured temp, but that is handled by an external controller now.

- [raspi-chill](#raspi-chill)
  - [setup](#setup)
  - [Tilt](#tilt)
  - [iSpindel](#ispindel)
  - [usage](#usage)
  - [hardware](#hardware)

## setup

`./install.sh`

## Tilt

https://github.com/frawau/aioblescan
also see https://github.com/baronbrew/TILTpi

install

```
sudo apt-get install bluetooth libbluetooth-dev
```

in src folder, install aioblescan with tilt plugin

```
wget https://github.com/baronbrew/aioblescan/archive/master.zip
unzip master.zip
cd aioblescan-master/
sudo -H python3 setup.py install
```

check that it works

```
sudo python3 -u -m aioblescan -T
```

## iSpindel

## usage

`nohup sudo ./src/regulate.py --name NAME &`

Real-time updates of `config.ini` are supported. Example usecase: change the regulation temperature, cycle time, ...

## hardware

- icebox v1: FreeCAD design and panels measurements in `cad/iceBox.fcstd`
- 12 VDC 80 mm fan
- 12 VDC relay
- Raspberry Pi 3
- Relay module
- 12 V at 400 mA power supply
- 5 V at 1A power supply
- Digital temperature sensor: DS18B20 (or XC3700 mounted on a board)
  - Reference: https://www.jaycar.com.au/digital-temperature-sensor-module/p/XC3700
  - Pinout: see ./docs for wiring
- (prototyping/debug only) Breadboard
- (prototyping/debug only) Jumper cables
