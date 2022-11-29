from time import time
class Settings:
    """A class to store all settings for under the sea"""
    def __init__(self):
        """Initialize the settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (255,255,255)

        # initially have 5 lives
        self.lives = 5

        # find the time the game starts
        self.time0 = int(time())

        # initially there are no special bubbles to capture
        self.special_on = False

        # initially there is no sparkle to shoot
        self.sparkleon = False

