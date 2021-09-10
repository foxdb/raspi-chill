# raspi-chill

- [raspi-chill](#raspi-chill)
  - [setup](#setup)
  - [Tilt](#tilt)
  - [iSpindel](#ispindel)
  - [usage](#usage)
  - [hardware](#hardware)
  - [icebox v2 (under development)](#icebox-v2-under-development)
    - [resources](#resources)
    - [components](#components)
      - [ice box](#ice-box)
      - [control, measurement and communications](#control-measurement-and-communications)
      - [power supply](#power-supply)
      - [heating system](#heating-system)
      - [cooling system](#cooling-system)
        **Continous mode:** monitors and maintain temperature

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

## icebox v2 (under development)

Why:

- I still live in a flat
- Still no room for a kegerator or a big fridge
- Still can't find a smaller bar fridge that will fit a 23/30L fermenter
- Tired of changing ice jugs every day
- Want to do lagers too: need more cold power than ice+fans
- icebox v1 was recycled when moved interstate
- icebox v1 was too expensive to build compared to buying a second hand fridge, mostly because of insulation panels

Goals:

- move away from ice jugs and install a powered cooling system
- build an insulated box with a smaller budget (original insulation panels costed ~80-100 dollars)
  - needs to fit in a closet
  - needs to be able to temp. control in the range: 5 to 30 degrees (MVP will be cooling only)

### resources

- state of the art in boat fridges cooling systems (12VDC): https://www.sailmagazine.com/diy/how-to-upgrading-your-icebox
- polystyren/foam ice-boxes: https://shop.powerpackaging.com.au/product-group/620-ice-pack-esky/category/2491-eskies

### components

#### ice box

> an icebox, built from combined existing foam-like eskys

Requirements:

- being reasonably insulated
- can host a 30L fermenter (Carboy-style, plastic)
- can fit in an appartment closet
- sustains reasonable liquid damage
- condensation?

Implementation:

Internal dimensions requirements:

- given fermenter size
- given internal cooling system size
- given electronics size

#### control, measurement and communications

> remotely configurable, real time control and data aggregation

Requirements:

- connected
  - hot-reloads configuration from various sources
  - start/stop over SSH
- regulation mode
- measure-only mode
- controls cold / hot elements

Implementation:

- raspberry pi
- DS18B20 temp. sensor for box internal temperature
- iSpindel for gravity and fermenter internal temperature
- relay

#### power supply

#### heating system

- heat cable + grill rack from IKEA
- in the range of 50-100

#### cooling system

Peltier or compressor refrigeration?

A DIY Peltier-based solution sounds a bit dangerous? And maybe not efficient enough.

Why not reusing the system out of a refrigerated esky

https://en.wikipedia.org/wiki/Thermoelectric_cooling

Implementations:
Compressor:

- strip existing cooling parts from an old fridge?
- boat-like or truck-like compressor-cooling kit?

Peltier:

- https://www.aliexpress.com/item/32971811480.html
- https://www.aliexpress.com/item/32946954579.html
- https://www.seafrost.com/BD.html

Esky-style:

- https://www.aliexpress.com/item/33040098056.html
