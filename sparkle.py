import pygame
from pygame.sprite import Sprite
from random import randint
from math import tan
from time import sleep

class Sparkle(Sprite):
    """A class to represent the sparkle that can be used to catch the bubbles"""
    def __init__(self, uts):
        """initialize the game and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the sparkle image and set its rect attribute

        self.image = pygame.image.load('sparkle.png')
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()

        # start each new sparkle on the diver
        self.rect.x = uts.diver.rect.x
        self.rect.y = uts.diver.rect.y

        # initialize the angle the sparkle will be traveling at
        self.pos = True
        self.theta = 0


    # print the sparkle
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # move the sparkle
    def move(self):
        if self.pos:
            self.rect.x += 20
            self.rect.y += 20 * tan(self.theta)
        else:
            self.rect.x -= 20
            self.rect.y -= 20 * tan(self.theta)



