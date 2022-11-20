class Settings:
    """A class to store all settings for under the sea"""
    def __init__(self):
        """Initialize the grids settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (255,255,255)

        # initially have 5 lives
        self.lives = 5

        #initially have a score of 0
        self.score = 0