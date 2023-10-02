# HD44780 LCD Controller Interface with MicroPython

https://github.com/Thomascountz/micropython_i2c_lcd/assets/19786848/07470ccc-1ee1-467d-855a-d67cb7de6779

This library provides an interface for controlling HD44780-based LCD displays using a PCF8574 I/O expander (often sold as a single module) with a MicroPython-compatible microcontroller. The library is designed to offer high-level functions for LCD control while allowing access to underlying GPIO operations on the PCF8574 when necessary.

## Overview

The library is structured around several classes, each serving a specific role:

1. `BacklightDriver`: An abstract base class for controlling the backlight of an LCD display.

2. `HD44780`: A class for interacting with HD44780 LCD drivers through a PCF8574 I/O expander. Provides methods for writing characters and strings to the LCD, clearing the display, and controlling the display properties.

3. `HD447804BitDriver`: An abstract base class for controlling the HD44780 LCD controller through a 4-bit data bus.

4. `HD447804BitPayload`: A class representing data to be written to the HD44780 LCD controller.

5. `LCD`: A high-level API for controlling HD44780-based LCD displays. This class provides methods to write text to the LCD, control the cursor and display properties, and clear the display.

6. `PCF8574`: A class for controlling the HD44780 LCD controller through a PCF8574 I/O expander. Implements the HD447804BitController and BacklightDriver interfaces, providing methods for writing 4-bit payloads to the HD44780 LCD controller via the PCF8574, and controlling the LCD's backlight.

7. `test_main`: Contains a function for testing the library's functionality.

## Usage

First, import the necessary classes from the library:

```python
from machine import Pin, I2C
from pcf8574 import PCF8574
from hd44780 import HD44780
from lcd import LCD
```

Then, initialize the LCD:

```python
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
pcf = PCF8574(i2c)
hd44780 = HD44780(pcf, num_lines=2, num_columns=16)
lcd = LCD(hd44780, pcf)
```

Now you can use the `lcd` object to control the LCD. For instance, to write a line of text to the display:

```python
lcd.write_line("Hello, world!", 0)
```

To create a scrolling text:

```python
lcd.marquee_text("Hello...", 1, 0.2)
```

To control the cursor and display:

```python
lcd.cursor_on()
lcd.blink_on()
utime.sleep(2)
lcd.cursor_off()
lcd.blink_off()
```

And to control the backlight:

```python
lcd.backlight_on()
utime.sleep(2)
lcd.backlight_off()
```

## Testing

Run the `main_test` function in `test_main.py` to verify the library's functionality. This function will run a series of tests to demonstrate the capabilities of the library.
