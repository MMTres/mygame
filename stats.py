import pygame
class Stats:
    """Track scores for under the sea"""
    def __init__(self, uts):
        """initialize stats"""
        self.settings = uts.settings
        self.screen = uts.screen

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
        #high score is not reset so it will save between plays
        self.livesleft = self.settings.lives
        self.score = 0

    def update_score(self):
        """display the current score on the screen"""
        #points r us code achievement
        font = pygame.font.Font('myfont.ttf', 50)
        img = font.render(f"Score: {self.score}", True, [200, 0, 100])
        self.screen.blit(img, (20, 15))

    def update_high_score(self):
        #over achiever code achievement
        """update the high score if the current score is bigger than the saved high score"""
        if self.score > self.high_score:
            self.high_score = self.score

    def display_high_score(self):
        """show the current high score on the screen"""
        #textual code achievement
        self.update_high_score()
        font = pygame.font.Font('myfont.ttf', 50)
        img = font.render(f"High Score: {self.high_score}", True, [200, 0, 100])
        self.screen.blit(img, (20, 55))






