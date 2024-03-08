from RPLCD.i2c import CharLCD
from time import sleep

I2C_ADDRESS = 0x27

lcd = CharLCD(i2c_expander='PCF8574', address=I2C_ADDRESS, port=1, cols=16, rows=2, dotsize=8)

def clear():
    lcd.clear()

def turn_backlight_off():
    lcd.backlight_enabled = False

def turn_backlight_on():
    lcd.backlight_enabled = True

def write(line1, line2):
    lcd.backlight_enabled = True
    lcd.clear()
    lcd.write_string(line1)
    lcd.crlf()
    lcd.write_string(line2)

def turn_off():
    lcd.clear()
    lcd.backlight_enabled = False
    lcd.close(clear=True)