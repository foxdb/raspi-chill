from RPLCD.i2c import CharLCD
from time import sleep

I2C_ADDRESS = 0x27

lcd = CharLCD(i2c_expander='PCF8574', address=I2C_ADDRESS, port=1, cols=16, rows=2, dotsize=8)

lcd.clear()

lcd.write_string('Hello, World!')
lcd.crlf()
lcd.write_string('Hold My Beer...')

sleep(5)

lcd.backlight_enabled = False
lcd.close(clear=True)