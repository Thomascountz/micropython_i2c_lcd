from hd44780 import HD44780
import utime


class LCD:
    """
    A high-level API for controlling HD44780-based LCD displays.

    This class provides methods to write text to the LCD, control the
    cursor and display properties, and clear the display.

    Usage:

    >>> lcd = LCD_Display(hd44780)
    >>> lcd.clear()
    >>> lcd.write_line(0, "Hello, world!")

    :param hd44780: An instance of the `HD44780` class.
    """

    def __init__(self, hd44780: HD44780):
        self.hd44780 = hd44780

    def get_hd44780(self):
        """
        Return the underlying HD44780 instance.

        This can be used by advanced users to access the lower-level functions of the HD44780 class.
        """
        return self.hd44780

    def clear(self):
        """
        Clear the LCD display.
        """
        self.hd44780.clear()

    def write_line(self, text: str, line: int = 0):
        """
        Write a string of text to a specific line on the LCD.

        If the string is longer than the number of columns, it will be clipped
        to fit on the line. If the string is shorter than the number of columns,
        the rest of the line will be filled with spaces.

        :param text: The text to write.
        :param line: The line number (0-based).
        """
        self.hd44780.set_cursor(line, 0)
        self.hd44780.write_string(text)

    def write_lines(self, text: str):
        """
        Write a string of text to the LCD, split into two lines.

        The string is split at the first '\n' character into two lines. If there
        is no '\n' character, the entire string is written to the first line and
        the second line is cleared.

        If the string contains more than one '\n' character, only the first one
        is used to split the string.

        :param text: The text to write.
        """
        # Split the text into two lines at the first '\n' character
        lines = text.split("\n", 1)

        # Write the first line to the LCD
        self.write_line(lines[0], 0)

        # If there is a second line, write it to the LCD
        if len(lines) > 1:
            self.write_line(lines[1], 1)
        else:
            # If there is no second line, clear the second line on the LCD
            self.write_line("", 1)

    def marquee_text(self, text: str, line: int = 0, delay: float = 0.2):
        """
        Display a line of text as a scrolling marquee on the LCD, using the auto-scroll feature.

        The text will appear from the right edge of the display and disappear at the left edge. The text will be
        scrolled from right to left automatically by the LCD's built-in auto-scroll feature. After the text has
        completely disappeared, it will start again from the right.

        :param text: The text to display.
        :param line: The line number (0-based) on which to display the marquee.
        :param delay: The delay, in seconds, between each step of the marquee. Default is 0.2 seconds.
        """
        # Pad the text with spaces on both sides equal to the width of the display
        text = " " * self.hd44780.num_columns + text + " " * self.hd44780.num_columns

        # Enable auto scroll
        self.hd44780.auto_scroll_on()

        # Write the entire text string to the display
        self.hd44780.set_cursor(line, 0)
        for char in text:
            self.hd44780.write_char(char)
            utime.sleep(delay)

        # Disable auto scroll
        self.hd44780.auto_scroll_off()

    def scroll_content_off_screen(self, direction: str = "right", delay: float = 0.2):
        """
        Scroll the current display content off the LCD to the specified edge.

        :param direction: The direction to which to exit the text. Can be 'left' or 'right'.
        :param delay: The delay, in seconds, between each step of the scroll. Default is 0.2 seconds.
        """
        for _ in range(self.hd44780.num_columns):
            if direction == "left":
                self.hd44780.move_left()
            else:
                self.hd44780.move_right()
            utime.sleep(delay)

    def display_on(self):
        """
        Turn on (unblank) the LCD.
        """
        self.hd44780.display_on()

    def display_off(self):
        """
        Turn off (blank) the LCD.
        """
        self.hd44780.display_off()

    def cursor_on(self):
        """
        Make the cursor visible.
        """
        self.hd44780.cursor_on()

    def cursor_off(self):
        """
        Make the cursor invisible.
        """
        self.hd44780.cursor_off()

    def blink_on(self):
        """
        Turn on the cursor blink.
        """
        self.hd44780.blink_on()

    def blink_off(self):
        """
        Turn off the cursor blink.
        """
        self.hd44780.blink_off()

    def backlight_on(self):
        """
        Turn on the LCD backlight.
        """
        self.hd44780.backlight_on()

    def backlight_off(self):
        """
        Turn off the LCD backlight.
        """
        self.hd44780.backlight_off()