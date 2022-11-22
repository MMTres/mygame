import random

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
from bubbles import Bubbles
from sparkle import Sparkle
from stats import Stats
from specialbubbles import SpecialBubbles


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
        self.bubbles = Bubbles(self)
        self.sparkleon = False
        self.stats = Stats(self)
        #self.spon = False
        self.sb = SpecialBubbles(self)

    def run_game(self):
        while True:


            self.reset_screen()
            self._check_events()
            if self.stats.game_active == True:
                self.update_puffer()
                self.update_little_fish()
                self.update_diver()
                self.check_mouse()
                self.update_sparkle()
                self.update_score()
                self.display_high_score()
                self.update_lives()
                self.bubbles.blitme()
                #self.update_sp_bubbles()v
                self.new_level()


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
        if self.lf.rect.x == self.screen.get_rect().right:
            self.lf.reset()
            self.smart_fish()

    def update_puffer(self):
        self.puffer.blitme()
        self.puffer.change_puffer_size()
        self.puffer.move()
        print(self.puffer.speed)
        sleep(0.05)
        if self.puffer.rect.x == self.screen.get_rect().left:
            self.puffer.reset()


    def update_sparkle(self):
        if self.sparkleon:
            self.sparkle.blitme()
            if self.bubbles.rect.x < self.diver.rect.x:
                self.sparkle.pos = False
            self.sparkle.move()
            self._caught_bubbles()

    #def update_sp_bubbles(self):
        #self.are_special_bubbles()
        #self.add_special_bubbles()
        #self._caught_sp()

    #def are_special_bubbles(self):
        #delay = random.randint(1000, 10000)
        #pygame.time.delay(delay)
        #self.spon = True
        #pygame.time.delay(3500)
        #self.spon = False

    def add_special_bubbles(self):
        if self.spon == True:
            self.sp.blitme()

    def smart_fish(self):
        """make the fish track the diver and swim towards them"""
        diver_position = [self.diver.rect.x, self.diver.rect.y]
        fish_position = [self.lf.rect.x, self.lf.rect.y]
        change_position = []
        for i in range(2):
            change_position.append(diver_position[i]-fish_position[i])
        self.lf.theta = atan(change_position[1]/change_position[0])

    def check_mouse(self):
        mouse = pygame.mouse.get_pos()
        if self.bubbles.rect.collidepoint(mouse):
            self.sparkleon = True
            self.sparkle = Sparkle(self)
            bubble_position = [self.bubbles.rect.x, self.bubbles.rect.y]
            sparkle_position = [self.sparkle.rect.x, self.sparkle.rect.y]
            change_position = []
            for i in range(2):
                change_position.append(bubble_position[i] - sparkle_position[i])
            if change_position[0] == 0:
                self.sparkle.vertical = True
            self.sparkle.theta = atan(change_position[1] / change_position[0])


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

    def _check_fish_diver_collisions(self):
        """respond to bullet-alien collisions"""
        #check for any fish that have hit the diver
        #if so lose a life
        if self.puffer.rect.colliderect(self.diver.rect) or self.lf.rect.colliderect(self.diver.rect):
            lost_life_sound = pygame.mixer.Sound("lostlife.wav")
            pygame.mixer.Sound.play(lost_life_sound)
            self.diver.restart_diver()
            self.puffer.reset()
            self.lf.reset()
            self.stats.livesleft -= 1

    def _caught_bubbles(self):
        """respond to bubble sparkle collisions"""
        #check if sparkle captured bubbles
        #if so increase score
        if self.sparkle.rect.colliderect(self.bubbles.rect):
            points_sound = pygame.mixer.Sound("sparkle.wav")
            pygame.mixer.Sound.play(points_sound)
            self.sparkleon = False
            self.stats.score += 10

            self.bubbles.reset()

    def _caught_sp(self):
        """respond to bullet-alien collisions"""
        # check if sparkle hit special bubbles
        # if so, regain a life
        if self.sparkle.rect.colliderect(self.sb.rect):
            self.sparkleon = False
            self.settings.lives += 1
            self.spon = False


    def new_level(self):
        if self.stats.score != 0 and self.stats.score % 100 == 0:
            print("yes")
            self.stats.score = self.stats.score + 10
            self.puffer.speed += 1
            self.lf.speed += 1
            self.puffer.reset()
            self.lf.reset()

    def high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score

    def display_high_score(self):
        self.high_score()
        font = pygame.font.SysFont('arial', 20)
        img = font.render(f"High Score: {self.stats.high_score}", True, [200, 0, 100])
        self.screen.blit(img, (20, 50))


    def update_score(self):
        font = pygame.font.SysFont('arial', 20)
        img = font.render(f"Score: {self.stats.score}", True, [200, 0, 100])
        self.screen.blit(img, (20, 20))

    def update_lives(self):
        self._check_fish_diver_collisions()
        x_value = 0
        if self.stats.livesleft == 0:
            self.stats.game_active = False

        for i in range(self.stats.livesleft):
            self.l.rect.x = self.screen.get_width() - 75 - 50 * i
            x_value +=1
            self.l.blitme()
        lost_lives = 5 - self.stats.livesleft
        for i in range(lost_lives):
            self.d.rect.x = self.screen.get_width() -75 -50 *x_value - 50 * i
            self.d.blitme()

if __name__ == '__main__':
    # make a game instance, and run the game
    uts = UnderTheSea()
    uts.run_game()
