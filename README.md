# HD44780 LCD Controller Interface with MicroPython

## Description

This library provides a programmatic interface for controlling HD44780-based LCD displays using a PCF8574 I/O expander in a MicroPython environment. The library is designed to offer convenient, high-level functions for LCD control while allowing access to underlying GPIO operations on PCF8574 when necessary.

## Classes

The library is built around three primary classes:

1. `LCD`: This class creates a more user-friendly API for controlling HD44780-based LCD displays. It wraps the `HD44780` class and provides utilities for operations like writing to specific LCD lines or creating scrolling texts.

2. `HD44780`: Interfaces directly with the HD44780 LCD controller via PCF8574 I/O expander. Offers methods for core operations like writing characters and strings, clearing display, and controlling display properties.

3. `PCF8574`: Facilitates interaction with the PCF8574 I/O expander using I2C protocol. It provides functions for reading from and writing to GPIO pins of the PCF8574.

## Usage

First, import the necessary classes from the library:

```python
from machine import Pin, I2C
from pcf8574 import PCF8574
from hd44780 import HD44780
from lcd import LCD
```

Initialize the LCD:

```python
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
pcf = PCF8574(i2c)
hd44780 = HD44780(pcf, num_lines=2, num_columns=16)
lcd = LCD(hd44780)
```

From here, you can use the `lcd` object to control the LCD. For instance, to write a line of text to the display:

```python
lcd.write_line("Hello, world!", 0)
```

To create a scrolling text:

```python
lcd.marquee_text("Hello...", 1, 0.2)
```

And to control the cursor and display:

```python
lcd.cursor_on()
lcd.blink_on()
utime.sleep(2)
lcd.cursor_off()
lcd.blink_off()
```
