import utime
from pcf8574 import PCF8574


class HD44780:
    """
    A class for interacting with HD44780 LCD controllers through a PCF8574 I/O expander.

    This class provides methods for writing characters and strings to the LCD,
    clearing the display, and controlling the display properties.

    Usage:

    >>> pcf = PCF8574(i2c)
    >>> lcd = HD44780(pcf, num_lines=2, num_columns=16)
    >>> lcd.clear()
    >>> lcd.write_string("Hello, world!")

    :param pcf: An instance of the `PCF8574` class.
    :param num_lines: The number of lines on the LCD.
    :param num_columns: The number of columns on the LCD.
    """

    # HD44780 LCD controller command set
    LCD_CLR = 0x01  # DB0: clear display
    LCD_HOME = 0x02  # DB1: return to home position
    LCD_ENTRY_MODE = 0x04  # DB2: set entry mode
    LCD_DISPLAY_CTRL = 0x08  # DB3: display control
    LCD_CURSOR_SHIFT = 0x10  # DB4: cursor shift
    LCD_FUNCTION_SET = 0x20  # DB5: function set
    LCD_SET_CGRAM_ADDR = 0x40  # DB6: set CG RAM address
    LCD_SET_DDRAM_ADDR = 0x80  # DB7: set DD RAM address

    # Flags for display on/off control
    LCD_ON_DISPLAY = 0x04  # DB2: turn display on
    LCD_ON_CURSOR = 0x02  # DB1: turn cursor on
    LCD_ON_BLINK = 0x01  # DB0: turn on cursor blink

    # Flags for display/cursor shift
    LCD_MOVE_DISP = 0x08  # DB3: move display (0-> move cursor)
    LCD_MOVE_RIGHT = 0x04  # DB2: move right (0-> left)

    # Flags for entry mode set
    LCD_ENTRY_INC = 0x02  # DB1: increment (cursor moves to the right)
    LCD_ENTRY_SHIFT = 0x01  # DB0: shift (enable automatic display shift)

    # Flags for function set
    LCD_8_BIT_MODE = 0x10  # DB4: 8-bit data length
    LCD_2_LINE = 0x08  # DB3: two line display
    LCD_5x10_DOTS = 0x04  # DB2: 5x10 dot character font

    # PCF8574 pin definitions
    PIN_RS = 0x01  # P0 - Register Select
    PIN_RW = 0x02  # P1 - Read/Write
    PIN_ENABLE = 0x04  # P2 - Enable bit
    BACKLIGHT_SHIFT = 3  # P3 - Backlight control
    DATA_SHIFT = 4  # P4-P7 - Data lines

    def __init__(self, pcf: PCF8574, num_lines: int, num_columns: int):
        self.pcf = pcf
        self.num_lines = min(num_lines, 4)
        self.num_columns = min(num_columns, 40)
        self.display_control = self.LCD_DISPLAY_CTRL | self.LCD_ON_DISPLAY
        self.entry_mode_set = self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC
        self.backlight = 0

        self._initialize()

    def _initialize(self):
        """
        Initialize the LCD in 4-bit mode and clear the display.

        This method performs the initialization sequence for the HD44780 controller
        in 4-bit mode according to the datasheet. The sequence involves switching
        to 8-bit mode first, repeating the 8-bit function set command three times
        (the first two with a delay), then switching to 4-bit mode. After the
        interface length is set, we send the function set command with the number
        of lines and character font size, clear the display, and set the entry mode.

        Time delays are incorporated at several steps in this sequence. These
        delays are necessary because the execution times for these commands are
        longer during the initialization process and we cannot check the busy flag
        during this time (as the interface is in the process of being set up).

        The specific timing values come from the HD44780 datasheet and are based on
        the worst-case times for each command.
        """
        # Wait for more than 40ms after power rises above 2.7V
        utime.sleep_ms(50)

        # Switch to 8-bit mode.
        # This is the first step of the initialization sequence.
        self._write_nibble(0x03)
        # The execution time for this command is longer during initialization,
        # so we wait for more than 4.1ms.
        utime.sleep_ms(5)

        # Repeat the function set command in 8-bit mode.
        self._write_nibble(0x03)
        # Again, the execution time for this command is longer during initialization,
        # so we wait for more than 100us.
        utime.sleep_us(150)

        # Repeat the function set command in 8-bit mode one more time.
        self._write_nibble(0x03)
        # We can use a shorter delay here.
        utime.sleep_ms(1)

        # Switch to 4-bit mode.
        # This is the second step of the initialization sequence.
        self._write_nibble(0x02)
        # We can use a shorter delay here.
        utime.sleep_ms(1)

        # Now that we're in 4-bit mode, we can set the number of display lines and
        # character font size with the function set command.
        # We use the LCD_2_LINE flag if the number of lines is more than one,
        # otherwise we don't set this flag (which defaults to one line).
        self._write_command(
            self.LCD_FUNCTION_SET | (self.LCD_2_LINE if self.num_lines > 1 else 0x00)
        )
        # We can use a shorter delay here.
        utime.sleep_ms(1)

        # Set the display control flags.
        # This command sets the display on/off, cursor on/off, and cursor blink on/off flags.
        # In this case, we're turning the display on and leaving the cursor and blink off.
        self._write_command(self.display_control)

        # Clear the display.
        self.clear()

        # Set the entry mode.
        # This command sets the direction that the cursor moves when we write data to the display.
        # In this case, we're incrementing the address counter (moving the cursor to the right)
        # and we're not shifting the display.
        self._write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)

    def _write_nibble(self, nibble: int):
        """
        Write a 4-bit nibble to the LCD through the PCF8574.
        """
        self.pcf.write((nibble & 0x0F) << self.DATA_SHIFT | self.PIN_ENABLE)
        self.pcf.write((nibble & 0x0F) << self.DATA_SHIFT)

    def clear(self):
        """
        Clear the LCD display and move the cursor to the top left corner.
        """
        self._write_command(self.LCD_CLR)
        self._write_command(self.LCD_HOME)

    def _write_command(self, cmd: int):
        """
        Write a command to the LCD.

        For 4-bit interface data, only four bus lines (DB4 to DB7) are used for transfer.
        Bus lines DB0 to DB3 are disabled. The data transfer between the HD44780 and the
        MPU is completed after the 4-bit data has been transferred twice. As for the order
        of data transfer, the four high order bits (for 8-bit operation, DB4 to DB7) are
        transferred before the four low order bits (for 8-bit operation, DB0 to DB3). The
        busy flag must be checked (one instruction) after the 4-bit data has been
        transferred twice. Two more 4-bit operations then transfer the busy flag and
        address counter data.

        The Register Select (RS) pin selects between data and instruction registers. If
        RS = 0, the instruction register is selected, allowing the user to send a command
        such as Clear Display, Return Cursor to Home, etc. If RS = 1, the data register
        is selected, allowing the user to send data to be displayed on the LCD.

        :param cmd: The command to write.
        """
        # Prepare high order bits and write them
        byte = (self.backlight << self.BACKLIGHT_SHIFT) | (
            ((cmd >> 4) & 0x0F) << self.DATA_SHIFT
        )
        self.pcf.write(byte | self.PIN_ENABLE)
        self.pcf.write(byte)

        # Prepare low order bits and write them
        byte = (self.backlight << self.BACKLIGHT_SHIFT) | (
            (cmd & 0x0F) << self.DATA_SHIFT
        )
        self.pcf.write(byte | self.PIN_ENABLE)
        self.pcf.write(byte)

        utime.sleep_ms(2)  # commands need > 37us to settle

    def write_char(self, char: str):
        """
        Write a character to the LCD at the current cursor position.

        :param char: The character to write.
        """
        self._write_data(ord(char))

    def write_string(self, text: str):
        """
        Write a string of text to the LCD at the current cursor position.

        If the string is longer than the number of columns, it will be clipped
        to fit on the current line. If the string is shorter than the number of
        columns, the rest of the line will be filled with spaces.

        :param text: The text to write.
        """
        for i in range(self.num_columns):
            if i < len(text):
                self.write_char(text[i])
            else:
                self.write_char(" ")

    def _write_data(self, data: int):
        """
        Write data to the LCD.

        For 4-bit interface data, only four bus lines (DB4 to DB7) are used for transfer.
        Bus lines DB0 to DB3 are disabled. The data transfer between the HD44780 and the
        MPU is completed after the 4-bit data has been transferred twice. As for the order
        of data transfer, the four high order bits (for 8-bit operation, DB4 to DB7) are
        transferred before the four low order bits (for 8-bit operation, DB0 to DB3). The
        busy flag must be checked (one instruction) after the 4-bit data has been
        transferred twice. Two more 4-bit operations then transfer the busy flag and
        address counter data.

        The Register Select (RS) pin selects between data and instruction registers. If
        RS = 0, the instruction register is selected, allowing the user to send a command
        such as Clear Display, Return Cursor to Home, etc. If RS = 1, the data register
        is selected, allowing the user to send data to be displayed on the LCD.

        :param data: The data to write.
        """
        # Prepare high order bits and write them
        byte = (
            self.PIN_RS
            | (self.backlight << self.BACKLIGHT_SHIFT)
            | (((data >> 4) & 0x0F) << self.DATA_SHIFT)
        )
        self.pcf.write(byte | self.PIN_ENABLE)
        self.pcf.write(byte)

        # Prepare low order bits and write them
        byte = (
            self.PIN_RS
            | (self.backlight << self.BACKLIGHT_SHIFT)
            | ((data & 0x0F) << self.DATA_SHIFT)
        )
        self.pcf.write(byte | self.PIN_ENABLE)
        self.pcf.write(byte)

        utime.sleep_us(50)  # data needs > 37us to settle

    def set_cursor(self, line: int, column: int):
        """
        Set the cursor position.

        :param line: The line number (0-based).
        :param column: The column number (0-based).
        """
        self._update_cursor(column, line)

    def _update_cursor(self, cursor_x: int, cursor_y: int):
        """
        Update the cursor position on the LCD.

        :param cursor_x: The column number (0-based).
        :param cursor_y: The line number (0-based).
        """
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40  # Lines 1 & 3 add 0x40
        if cursor_y & 2:  # Lines 2 & 3 add number of columns
            addr += self.num_columns
        self._write_command(self.LCD_SET_DDRAM_ADDR | addr)

    def display_on(self):
        """
        Turn on (unblank) the LCD.
        """
        self.display_control |= self.LCD_ON_DISPLAY
        self._write_command(self.display_control)

    def display_off(self):
        """
        Turn off (blank) the LCD.
        """
        self.display_control &= ~self.LCD_ON_DISPLAY
        self._write_command(self.display_control)

    def cursor_on(self):
        """
        Make the cursor visible.
        """
        self.display_control |= self.LCD_ON_CURSOR
        self._write_command(self.display_control)

    def cursor_off(self):
        """
        Make the cursor invisible.
        """
        self.display_control &= ~self.LCD_ON_CURSOR
        self._write_command(self.display_control)

    def blink_on(self):
        """
        Turn on the cursor blink.
        """
        self.display_control |= self.LCD_ON_BLINK
        self._write_command(self.display_control)

    def blink_off(self):
        """
        Turn off the cursor blink.
        """
        self.display_control &= ~self.LCD_ON_BLINK
        self._write_command(self.display_control)

    def move_left(self):
        """
        Shift the display to the left without changing the DDRAM content.
        """
        self._write_command(self.LCD_CURSOR_SHIFT | self.LCD_MOVE_DISP)

    def move_right(self):
        """
        Shift the display to the right without changing the DDRAM content.
        """
        self._write_command(
            self.LCD_CURSOR_SHIFT | self.LCD_MOVE_DISP | self.LCD_MOVE_RIGHT
        )

    def auto_scroll_on(self):
        """
        Enable automatic display shift after each character is written.
        """
        self.entry_mode_set |= self.LCD_ENTRY_SHIFT
        self._write_command(self.entry_mode_set)

    def auto_scroll_off(self):
        """
        Disable automatic display shift.
        """
        self.entry_mode_set &= ~self.LCD_ENTRY_SHIFT
        self._write_command(self.entry_mode_set)

    def backlight_on(self):
        """
        Turn on the backlight.
        """
        self.backlight = 1
        self.pcf.write(self.backlight << self.BACKLIGHT_SHIFT)

    def backlight_off(self):
        """
        Turn off the backlight.
        """
        self.backlight = 0
        self.pcf.write(self.backlight << self.BACKLIGHT_SHIFT)
