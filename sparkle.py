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

        # start each new puffer on the left of the screen in a random spot
        self.rect.x = 0
        self.rect.y = 0

        #initialize the sparkle to be off
        self.sparkleon = False

        # initialize the angle the sparkle will be traveling at
        self.theta = 0

    # print the sparkle
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # move the sparkle
    def move(self):
        self.hit_edge()
        self.rect.x += 20
        self.rect.y += 20 * tan(self.theta)


