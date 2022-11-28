import pygame
from pygame.sprite import Sprite

class LostLife(Sprite):
    """A class to represent a lost life"""
    def __init__(self, uts):
        """initialize and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the death image and set its rect attribute
        self.image = pygame.image.load('images/fishTile_096.png')
        self.image = pygame.transform.scale(self.image, (35, 50))
        self.rect = self.image.get_rect()

        # start each new puffer on the top right of the screen
        self.rect.x = self.screen_rect.left
        self.rect.y = self.screen_rect.top + 10

    def blitme(self):
        """print the lost life"""
        self.screen.blit(self.image, self.rect)