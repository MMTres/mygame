import pygame
import sys
from time import sleep, time
from settings import Settings
from puffer import Puffer
from diver import Diver
from littlefish import LittleFish
from math import atan
from life import Life
from lostlife import LostLife


class UnderTheSea:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Under the Sea")

        #initialize the game screen
        self.image = pygame.image.load('underthesea.bmp')
        self.image = pygame.transform.scale(self.image, (1200, 600))
        self.screen.blit(self.image, (0, 0))



        #initialize the sprites
        self.puffer = Puffer(self)
        self.diver = Diver(self)
        self.lf = LittleFish(self)
        self.l = Life(self)
        self.d = LostLife(self)
        self.smart_fish()


        #initially have 3 lives
        self.lives = 3


    def run_game(self):
        while True:

            self.reset_screen()
            self.update_puffer()
            self._check_events()
            self.update_little_fish()
            self.update_diver()
            self.update_score()
            self.update_lives()


            pygame.display.flip()

    def reset_screen(self):
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.image, (0, 0))

    def update_diver(self):
        self.diver.check_edges()
        self.diver.blitme()

    def update_little_fish(self):
        self.lf.move()
        self.lf.blitme()

    def update_puffer(self):
        self.puffer.blitme()
        self.puffer.change_puffer_size()
        self.puffer.move()
        sleep(0.05)

    def smart_fish(self):
        """make the fish track the diver and swim towards them"""
        diver_position = [self.diver.rect.x, self.diver.rect.y]
        fish_position = [self.lf.rect.x, self.lf.rect.y]
        change_position = []
        for i in range(2):
            change_position.append(diver_position[i]-fish_position[i])
        print(change_position)
        self.lf.theta = atan(change_position[1]/change_position[0])
        print(self.lf.theta)


    def _check_events(self):
        """respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_UP:
            #diver jumps
            self.diver.jump()
            self.diver.gravity = True
        elif event.key == pygame.K_q:
            sys.exit()

    def update_score(self):
        score = 100
        font = pygame.font.SysFont('arial', 20)
        img = font.render(f"Score: {score}", True, (255, 0, 100))
        self.screen.blit(img, (20, 20))

    def update_lives(self):
        for i in range(self.lives):
            self.l.rect.x = self.screen.get_width() - 75 - 50 * i
            x_value = self.l.rect.x
            self.l.blitme()
        lost_lives = 3 - self.lives
        for i in range(lost_lives):
            self.d.rect.x = x_value - 50 - 50 * i
            self.d.blitme()


if __name__ == '__main__':
    # make a game instance, and run the game
    uts = UnderTheSea()
    uts.run_game()
