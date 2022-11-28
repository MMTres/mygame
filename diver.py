import pygame


class Diver:
    """A class to manage the diver"""

    def __init__(self, uts):
        """Initialize the ship and set its starting position"""
        self.screen = uts.screen
        self.settings = uts.settings
        self.screen_rect = uts.screen.get_rect()

        # load the diver image and get its rect
        self.image = pygame.image.load('images/diver.png')
        self.image = pygame.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect()

        # put the diver at the bottom middle of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        print(self.rect.y)

        #store a decimal value for the diver's vertical speed
        self.diver_speed = 0

        #initialize the diver's gravity
        self.gravity = False


    def restart_diver(self):
        """put the diver back on the bottom middle of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.gravity = False


    def blitme(self):
        """Draw the diver at its current location"""
        if self.gravity:
            self._gravity()
        self.screen.blit(self.image, self.rect)

    def jump(self):
        """change the divers velocity when they jump"""
        self.diver_speed = -200

    def _gravity(self):
        """create gravity for the diver"""
        #velocity final = velocity initial plus acceleration * time
        self.diver_speed += 100 * 0.3
        # position = velocity * time
        self.rect.y += self.diver_speed * 0.3

    def check_edges(self):
        """restart diver if he is touching an edge"""
        if self.rect.y >= 600:
            self.restart_diver()
        if self.rect.y < 0:
            self.rect.y = 0

    def instruction_screen(self):
        """print the diver to the instruction screen"""
        self.rect.x = 300
        self.rect.y = 150
        self.screen.blit(self.image, self.rect)

