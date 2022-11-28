import pygame
from pygame.sprite import Sprite
from random import randint

class Bubbles(Sprite):
    """A class to represent a bubbles"""
    def __init__(self, uts):
        """initialize the bubble and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #load the bubble image and set its rect attribute
        self.image = pygame.image.load('images/bubbles2.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()


        # start each new puffer on the left of the screen in a random spot
        self.rect.x = randint(0, self.screen_rect.right -50)
        self.rect.y = randint(0, self.screen_rect.bottom -50)


    def blitme(self):
        """print the bubbles"""
        self.screen.blit(self.image, self.rect)

    def reset(self):
        """set the bubbles in a new random location"""
        self.rect.x = randint(0, self.screen_rect.right -50)
        self.rect.y = randint(0, self.screen_rect.bottom-50)
        #do not let the bubbles be directly above or below the diver
        if self.rect.x in range(500, 700):
            if self.rect.x < 600:
                self.rect.x -= 100
            else:
                self.rect.x += 100
        print(self.rect.x)

    def instruction_screen(self):
        """print the bubbles on the instruction screen"""
        self.rect.x = 500
        self.rect.y = 300
        self.blitme()


