# raspi-chill

## Setup

- `./install.sh`

## Usage

**Continous mode:** monitors and maintain temperature

`nohup sudo ./src/regulate.py --name NAME &`

Real-time updates of `config.ini` are supported. Example usecase: change the regulation temperature, cycle time, ...

## Hardware

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

## v2 hardware (under development)

Goals:

- move away from ice jugs (too much maintenance) and install a compressor-based cooling system
- re-build an insulated box with a smaller budget (original insulation panels costed ~80-100 dollars)

### resources

- state of the art in boat cooling systems (12VDC): https://www.sailmagazine.com/diy/how-to-upgrading-your-icebox
- example polystyren ice-boxes: https://shop.powerpackaging.com.au/product-group/620-ice-pack-esky/category/2491-eskies

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

#### cooling system

Implementations:
- strip existing cooling parts from an old fridge?
- boat-like or truck-like compressor-cooling kit?
