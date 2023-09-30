from machine import I2C


class PCF8574:
    """
    A class for interacting with the PCF8574 I2C I/O expander.

    This class provides a simple API for reading from and writing to the GPIO pins
    of the PCF8574. It is specifically designed for communicating
    with an HD44780 LCD controller through the PCF8574.

    Usage:

    >>> i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    >>> pcf = PCF8574(i2c)
    >>> pcf.write(0x0F)  # write 0x0F to the GPIO register
    >>> print(pcf.read())  # read the GPIO register

    :param i2c: An instance of the `machine.I2C` class representing the I2C bus.
    :param address: The I2C address of the PCF8574. Defaults to 0x27.
    """

    def __init__(self, i2c: I2C, address: int = 0x27):
        self.i2c = i2c
        self.address = address
        self._gpio_state = bytearray(1)  # store the current GPIO state

    def write(self, data: int):
        """
        Write an 8-bit value to the GPIO register of the PCF8574.

        Note that this method will write to the entire register, affecting all GPIO pins.

        :param data: The 8-bit value to write to the GPIO register.
        """
        self._gpio_state[0] = data & 0xFF
        self.i2c.writeto(self.address, self._gpio_state)
