import pygame
from pygame.sprite import Sprite
from random import randint
from time import sleep


class SpecialBubbles(Sprite):
    """A class to represent a bubbles"""
    def __init__(self, uts):
        """initialize the bubble and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the bubble image and set its rect attribute

        self.image = pygame.image.load('images/greenbubbles.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()


        # start each new puffer on the left of the screen in a random spot
        self.rect.x = randint(0, self.screen_rect.right -10)
        self.rect.y = randint(0, self.screen_rect.bottom -10)


    def blitme(self):
        """print the bubbles"""
        self.screen.blit(self.image, self.rect)

    def reset(self):
        """reset the bubbles to a random spot on the screen"""
        self.rect.x = randint(0, self.screen_rect.right -50)
        self.rect.y = randint(0, self.screen_rect.bottom-50)

