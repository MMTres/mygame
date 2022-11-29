import pygame
from pygame.sprite import Sprite
from random import randint
from math import tan, atan


class LittleFish(Sprite):
    """A class to represent a little fish that attacks the diver"""
    def __init__(self, uts):
        """initialize fish attributes and set its starting position"""
        super().__init__()
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()
        self.diver = uts.diver

        #load the puffer image and set its rect attribute
        self.image = pygame.image.load('images/fishTile_075.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        # start each new puffer on the left of the screen in a random spot
        self.rect.x = self.screen_rect.left
        self.rect.y = randint(0, self.screen_rect.bottom)

        #initialize the angle the fish will be traveling at
        self.theta = 0

        #initialize the speed of the fish
        self.speed = 1

        #set the fish to track the diver
        self.smart_fish()

    def draw(self):
        """print the little fish"""
        self.screen.blit(self.image, self.rect)

    def move(self):
        """move the fish based on the calculated angle of attack"""
        #check if the fish has hit the edge to see if theta changes
        self.hit_edge()
        #have the change and position vary with the speed (determined by the level)
        self.rect.x += 10 + 10* self.speed
        self.rect.y += (10 + 10* self.speed) * tan(self.theta)

    def reset(self):
        """reset the fish after it hits the diver or touches the edge of the screen"""
        self.rect.x = self.screen_rect.left
        self.rect.y = randint(0, self.screen_rect.bottom)
        self.theta = 0


    def hit_edge(self):
        """if the fish hits the top or bottom of the screen, make it bounce off"""
        if self.rect.bottom > self.screen_rect.bottom or self.rect.top < 0:
            self.theta = -1 * self.theta

    def instruction_screen(self):
        """print the little fish to the instruction screen"""
        self.rect.x = 750
        self.rect.y = 150
        self.draw()

    def smart_fish(self):
        """make the fish track the diver and swim towards them"""
        #terminator code achievement
        #tricky trig code achievement
        diver_position = [self.diver.rect.x, self.diver.rect.y]
        fish_position = [self.rect.x, self.rect.y]
        change_position = []
        for i in range(2):
            #find the x and y distance the fish needs to go to hit the diver
            change_position.append(diver_position[i]-fish_position[i])
        #find the angle the fish needs to go to hit the diver
        self.theta = atan(change_position[1]/change_position[0])

    def update_little_fish(self):
        """update the small fish's postion"""
        self.move()
        self.draw()
        # if the little fish has hit the edge of the screen,
        if self.rect.x == self.screen.get_rect().right:
            self.reset()
            self.smart_fish()




