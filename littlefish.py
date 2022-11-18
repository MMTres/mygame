import pygame
from pygame.sprite import Sprite
from random import randint
from math import tan
from time import sleep

class LittleFish(Sprite):
    """A class to represent a single alien in the fleet"""
    def __init__(self, uts):
        """initialize the game and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the puffer image and set its rect attribute

        self.image = pygame.image.load('fishTile_073.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()


        # start each new puffer on the left of the screen in a random spot
        self.rect.x = self.screen_rect.left
        self.rect.y = randint(0, self.screen_rect.bottom)

        #initialize the angle the fish will be traveling at
        self.theta = 0

        self.speed = 1

    #print the puffer
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    #move the fish
    def move(self):
        self.hit_edge()
        self.rect.x += 10 + 10* self.speed
        self.rect.y += (10 + 10* self.speed) * tan(self.theta)

    def reset(self):
        self.rect.x = self.screen_rect.left
        self.rect.y = randint(0, self.screen_rect.bottom)
        self.theta = 0

    #if the fish hits the top or bottom of the screen, make it bounce off
    def hit_edge(self):
        if self.rect.bottom > self.screen_rect.bottom or self.rect.top < 0:
            self.theta = -1 * self.theta


