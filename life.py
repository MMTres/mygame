import pygame
from pygame.sprite import Sprite

class Life(Sprite):
    """A class to represent a single alien in the fleet"""
    def __init__(self, uts):
        """initialize the game and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the lifeimage and set its rect attribute
        self.image = pygame.image.load('images/fishTile_077.png')
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()

        # put each new life on the upper right of the screen
        self.rect.x = self.screen_rect.right
        self.rect.y = self.screen_rect.top + 10

    def draw(self):
        """print the life"""
        self.screen.blit(self.image, self.rect)



