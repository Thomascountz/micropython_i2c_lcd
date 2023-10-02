from hd44780_4bit_payload import HD447804BitPayload


class HD447804BitDriver:
    """
    An interface for controlling the HD44780 LCD controller through a 4-bit data bus.
    """

    def write(self, payload: HD447804BitPayload):
        raise NotImplementedError
