class BacklightDriver:
    """
    An interface for controlling the backlight of an LCD display.
    """

    def backlight_on(self):
        raise NotImplementedError

    def backlight_off(self):
        raise NotImplementedError
