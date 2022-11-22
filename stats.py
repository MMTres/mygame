class Stats:
    """Track scores for under the sea"""

    def __init__(self, uts):
        """initialize stats"""
        self.settings = uts.settings
        self.game_active = True
        self.high_score = 0
        self.level = 1
        self.reset_stats()
        # initially have a score of 0
        self.score = 0

    def reset_stats(self):
        self.livesleft = self.settings.lives

