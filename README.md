# raspi-chill

Raspi-chill on Raspberry Pi:

- Accepts data sent via HTTP from iSpindels (wifi)
- Gathers data from nearby Tilts (bluetooth)
- Forwards data to the **Hold My Beer** platform
- Exposes a local brewery UI to get real time data from nearby sensors

Previously was also a temp. controller (ice box - fermentation chiller, turning a fan on/off). That is handled by an external controller now.

- [raspi-chill](#raspi-chill)
  - [setup](#setup)
    - [crontab setup](#crontab-setup)
  - [usage](#usage)
  - [tilt support](#tilt-support)
  - [LCD support](#lcd-support)
  - [hardware - deprecated](#hardware---deprecated)

## setup

Install python deps, bluetooth, i2c... Make sure I2C is enabled (`raspy-config`).

```
pip install -r requirements.txt
cp src/config.example.ini src/config.ini
mkdir logs
sudo apt-get install -y i2c-tools python3-smbus
sudo apt-get install bluetooth libbluetooth-dev
```

Make sure `remote/s3-upload.sh` exists. Need aws credentials setup (aws config).

### crontab setup

On system boot, start the main regulation system. Once an hour, refresh config file from S3.

As root, `crontab -e`:

```
*/5 * * * * /home/pi/projects/raspi-chill/remote/s3-upload.sh
@reboot sleep 5 && nohup sudo python3 /home/pi/projects/raspi-chill/src/regulate.py &
```

## usage

`nohup sudo ./src/regulate.py --name NAME &`

Real-time updates of `config.ini` are supported. Example usecase: change the regulation temperature, cycle time, ...

## tilt support

https://github.com/frawau/aioblescan
also see https://github.com/baronbrew/TILTpi

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

## LCD support

2 rows / 16 chars per row

Test:

```
python3 src/test_lcd_display.py
```

check if i2c is loaded: `lsmod | grep i2c_`
get address of the i2c backpack: `sudo i2cdetect -y 1`

usually `0x27`

docs: https://rplcd.readthedocs.io/en/stable/usage.html

## hardware - deprecated

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
