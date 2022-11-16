import pygame
from pygame.sprite import Sprite
from random import randint
from math import sin, pi
from time import sleep

class Puffer(Sprite):
    """A class to represent a single alien in the fleet"""
    def __init__(self, uts):
        """initialize the game and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the puffer image and set its rect attribute

        self.image = pygame.image.load('puffer2.bmp')
        self.image = pygame.transform.scale(self.image, (100, 100))

        #make a copy of the image for future scaling
        self.image2 = self.image
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        # start each new puffer on the left of the screen in a random spot
        self.rect.x = self.screen_rect.right
        self.rect.y = randint(0, self.screen_rect.bottom)

        #initial size of the fish
        self.size = 100

        #shrink value, 1 means grow, -1 means shrink
        self.shrink = 1

        #used for sin curve for puffer
        self.n =0

    #pring the puffer
    def blitme(self):
        self.screen.blit(self.image2, self.rect)

    #determine if the puffer is growing or shrinking
    def _grow_or_shrink(self):
        if self.size == 200 or self.size == 50:
            self.shrink *= -1

    #change the size of the puffer
    def change_puffer_size(self):
        self._grow_or_shrink()
        if self.shrink == 1:
            self.size = self.size +10
        else:
            self.size = self.size-10
        self.image2 = pygame.transform.scale(self.image, (self.size,self.size))

    #move the puffer in a sin curve
    def move(self):
        trig_list = [pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4, 2*pi]

        self.rect.x -= 10
        self.rect.y = 100 + 50*sin(trig_list[self.n])
        if self.n < 7:
            self.n = self.n+1
        else:
            self.n=0












