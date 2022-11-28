class Stats:
    """Track scores for under the sea"""

    def __init__(self, uts):
        """initialize stats"""
        self.settings = uts.settings

        #initialize game to be inactive so the instructions screen appears
        self.game_active = False

        #initialize the high score to 0
        self.high_score = 0

        #start the game on the first level
        self.level = 1

        #reset the game stats to find number of lives
        self.reset_stats()

        # initially have a score of 0
        self.score = 0

    def reset_stats(self):
        """reset the game statistics"""
        self.livesleft = self.settings.lives
        self.score = 0

