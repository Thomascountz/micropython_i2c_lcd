from machine import Pin, I2C
import utime
from pcf8574 import PCF8574
from hd44780 import HD44780
from lcd import LCD


def main_test():
    print("Create an I2C object")
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

    print("Create a PCF8574 object")
    pcf = PCF8574(i2c)

    print("Create an HD44780 object")
    hd44780 = HD44780(pcf, num_lines=2, num_columns=16)

    print("Create an LCD object")
    lcd = LCD(hd44780)

    while True:
        print("Turn on backlight")
        lcd.backlight_on()

        print("Test writing a string to the first line of the LCD")
        lcd.write_line("Hello, world!", 0)

        print("Test writing a string to the second line of the LCD")
        lcd.write_line("This is a test", 1)

        print("Wait for a while")
        utime.sleep(2)

        print("Test moving the display content to the right and then to the left")
        lcd.scroll_content_off_screen("left", 0.2)
        lcd.scroll_content_off_screen("right", 0.2)

        print("Test blinking the cursor")
        hd44780.set_cursor(0, 0)
        lcd.cursor_on()
        lcd.blink_on()
        utime.sleep(2)

        print("Test hiding the cursor")
        lcd.cursor_off()
        lcd.blink_off()

        print("Test turning off and on the display")
        lcd.display_off()
        utime.sleep(2)
        lcd.display_on()

        print("Test scrolling a text as a marquee on the second line")
        lcd.clear()
        lcd.marquee_text("Hello...", 1, 0.2)

        print("Test writing two lines of text at once")
        lcd.write_lines("First line\nSecond line")

        print("Wait for a while")
        utime.sleep(2)

        print("Clear the LCD")
        lcd.clear()

        print("Test turning on and off the backlight")
        lcd.backlight_off()
        utime.sleep(3)
        lcd.backlight_on()

        print(
            "Write a string to the first line of the LCD to indicate that the test is completed"
        )
        lcd.write_line("Test completed", 0)

        print("Wait for a while")
        utime.sleep(2)

        print("Clear the LCD at the end of each loop iteration")
        lcd.clear()


if __name__ == "__main__":
    main_test()
