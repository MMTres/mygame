import pygame
from pygame.sprite import Sprite

class LostLife(Sprite):
    """A class to represent a single alien in the fleet"""
    def __init__(self, uts):
        """initialize the game and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the death image and set its rect attribute
        self.image = pygame.image.load('fishTile_096.png')
        self.image = pygame.transform.scale(self.image, (35, 50))
        self.rect = self.image.get_rect()

        # start each new puffer on the top right of the screen
        self.rect.x = self.screen_rect.left
        self.rect.y = self.screen_rect.top

    #print the life
    def blitme(self):
        self.screen.blit(self.image, self.rect)