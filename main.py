from machine import Pin, I2C
from pcf8574 import PCF8574
from hd44780 import HD44780
from lcd import LCD


def main():
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    pcf8574 = PCF8574(i2c)
    hd44780 = HD44780(pcf8574, num_lines=2, num_columns=16)
    lcd = LCD(hd44780, pcf8574)
    lcd.backlight_on()
    lcd.write_lines("Hello, world!\nCountz Research")


if __name__ == "__main__":
    main()
