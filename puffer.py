import pygame
from pygame.sprite import Sprite
import random
from math import sin, pi

class Puffer(Sprite):
    """A class to represent a single puffer in the fleet"""
    def __init__(self, uts):
        """initialize the puffer and its attributes"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the puffer image
        self.image = pygame.image.load('images/puffer2.bmp')
        self.image = pygame.transform.scale(self.image, (100, 100))

        #make a copy of the image for future scaling
        self.image2 = self.image
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        # start each new puffer on the right of the screen in a random spot
        self.rect.x = self.screen_rect.right
        self.rect.y = random.randint(0, self.screen_rect.bottom)
        self.ycopy = self.rect.y

        #initial size of the fish
        self.size = 100

        #shrink value, 1 means grow, -1 means shrink
        self.shrink = 1

        #used for sin curve for puffer
        self.n =0

        #initialize the speed of the fish
        self.speed = 1

    def blitme(self):
        """print the puffer"""
        self.screen.blit(self.image2, self.rect)

    def _grow_or_shrink(self):
        """determine if the puffer is growing or shrinking"""
        if self.size == 200 or self.size == 50:
            self.shrink *= -1

    def change_puffer_size(self):
        """change the size of the puffer"""
        self._grow_or_shrink()
        if self.shrink == 1:
            self.size = self.size +10
        else:
            self.size = self.size-10
        self.image2 = pygame.transform.scale(self.image, (self.size,self.size))


    def move(self):
        """move the puffer in a sin curve"""
        trig_list = [pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4, 2*pi]
        #change the x position based on the puffer's speed (based on the level)
        self.rect.x -= 5 + self.speed * 5
        #change the y position in a sin curve
        self.rect.y = self.ycopy + 50*sin(trig_list[self.n])
        #iterate through the trig list
        #once the entire trig list has been passed through, start over
        if self.n < 7:
            self.n = self.n+1
        else:
            self.n=0

    def reset(self):
        """reset the puffer image to a random spot on the right of the screen"""
        self.rect.x = self.screen_rect.right
        self.rect.y = random.randint(0, self.screen_rect.bottom)
        self.ycopy = self.rect.y

    def reset_speed(self):
        """reset the puffer's speed"""
        self.speed = 1

    def instruction_screen(self):
        """print the puffer to the instruction screen"""
        self.rect.x = 900
        self.rect.y = 210
        self.blitme()













