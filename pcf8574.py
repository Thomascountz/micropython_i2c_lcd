from machine import I2C
from hd44780_4bit_payload import HD447804BitPayload
from hd44780_4bit_driver import HD447804BitDriver
from backlight_driver import BacklightDriver
import utime


class PCF8574(HD447804BitDriver, BacklightDriver):
    """
    A class for controlling the HD44780 LCD controller through a PCF8574 I/O expander.

    This class implements the HD447804BitController interface, providing methods for
    writing 4-bit payloads to the HD44780 LCD controller via the PCF8574.

    Usage:

    >>> i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    >>> pcf = PCF8574(i2c)
    >>> pcf.write(HD447804BitPayload(e=1, rs=0, rw=0, data=0x0F))

    :param i2c: An instance of the `machine.I2C` class representing the I2C bus.
    :param address: The I2C address of the PCF8574. Defaults to 0x27.
    """

    # PCF8574 device address
    DEFAULT_ADDRESS = 0x27

    # PCF8574 <-> HD44780 byte shifts
    RS_SHIFT = 0  # P0 - Register Select
    RW_SHIFT = 1  # P1 - Read/Write
    ENABLE_SHIFT = 2  # P2 - Enable bit
    DATA_SHIFT = 4  # P4-P7 - Data lines

    # PCF8574 <-> Backlight byte shift
    BACKLIGHT_SHIFT = 3  # P3 - Backlight control

    def __init__(self, i2c: I2C, address: int = DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.backlight = 0  # backlight is initially off

    def write(self, payload: HD447804BitPayload):
        """
        Write a 4-bit payload to the HD44780 LCD controller through the PCF8574.

        This method prepares a byte to be sent to the hardware, consisting of the
        4-bit payload and control signals for the HD44780 LCD controller, and the
        backlight control pin connected to the PCF8574. The byte is then sent to
        the I2C interface.

        :param payload: An instance of the HD447804BitPayload class.
        """

        byte = (
            self.backlight << self.BACKLIGHT_SHIFT
            | payload.e << self.ENABLE_SHIFT
            | payload.rs << self.RS_SHIFT
            | payload.rw << self.RW_SHIFT
            | payload.data << self.DATA_SHIFT
        )
        self._write_byte(byte)

    def backlight_on(self):
        """
        Turn the backlight on.

        This method sets the backlight control pin connected to the PCF8574 to 1.
        This does not effect the state of the HD44780 LCD controller because the
        E pin is not set.
        """
        self.backlight = 1
        self._write_byte(self.backlight << self.BACKLIGHT_SHIFT)

    def backlight_off(self):
        """
        Turn the backlight off.

        This method sets the backlight control pin connected to the PCF8574 to 0.
        This does not effect the state of the HD44780 LCD controller because the
        E pin is not set.
        """
        self.backlight = 0
        self._write_byte(self.backlight << self.BACKLIGHT_SHIFT)

    def _write_byte(self, byte: int):
        """
        Write a byte to the I2C bus.

        This method writes a byte to the I2C bus, using the address of the PCF8574.

        :param byte: The byte to write to the I2C bus.
        """
        # print("Writing byte:  b'{:08b}'".format(byte & 0xFF))
        utime.sleep_ms(1)
        self.i2c.writeto(self.address, bytes([byte & 0xFF]))
