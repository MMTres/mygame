import pygame
from pygame.sprite import Sprite
from random import randint
from time import time


class SpecialBubbles(Sprite):
    """A class to represent a bubbles"""
    def __init__(self, uts):
        """initialize the bubble and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = uts.settings

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
        #use -50 to keep them from being too close to the side of the screen
        self.rect.x = randint(0, self.screen_rect.right -50)
        self.rect.y = randint(0, self.screen_rect.bottom-50)

    def update_sp_bubbles(self):
        """update the special bubbles"""
        #special bubbles are a powerup that returns a life to the player
        self.are_special_bubbles()
        self.add_special_bubbles()

    def are_special_bubbles(self):
        """use a timer to turn the special bubbles on and off"""
        #tick tock code achievement
        time1 = int(time())
        #turn the bubbles on every 10 seconds for 3 seconds using modulus
        if (time1 - self.settings.time0) % 10 == 3:
            self.settings.special_on = True
        if (time1 - self.settings.time0) % 10 == 6:
            self.settings.special_on = False
            self.reset()

    def add_special_bubbles(self):
        """if the special bubbles are on, print them"""
        if self.settings.special_on == True:
            self.blitme()

    def instruction_screen(self):
        """print the little fish to the instruction screen"""
        self.rect.x = 775
        self.rect.y = 400
        self.blitme()

