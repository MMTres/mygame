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
from play import PlayButton


class UnderTheSea:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Under the Sea")

        #initialize the game screen
        self.image = pygame.image.load('images/underthesea.bmp')
        self.image = pygame.transform.scale(self.image, (1200, 600))
        self.screen.blit(self.image, (0, 0))


        #initialize the sprites
        self.puffer = Puffer(self)
        self.diver = Diver(self)
        self.lf = LittleFish(self)
        self.l = Life(self)
        self.d = LostLife(self)
        self.bubbles = Bubbles(self)
        self.sp = SpecialBubbles(self)


        #initially there is no sparkle to shoot
        self.sparkleon = False

        #initialize the game statistics
        self.stats = Stats(self)

        #initially there are no special bubbles to capture
        self.spon = False

        #create the play button
        self.play = PlayButton(self)

        #initialize the fish to track the diver
        self.smart_fish()

        #find the time the game starts
        self.time0 = int(time())


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
                self.update_sp_bubbles()
                self.new_level()
            else:

                self.instructions_screen()
                self.play.draw_button()


            pygame.display.flip()

    def reset_screen(self):
        """reset the screen's background"""
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.image, (0, 0))

    def update_diver(self):
        """update the diver's location"""
        self.diver.check_edges()
        self.diver.blitme()

    def update_little_fish(self):
        """update the small fish's postion"""
        self.lf.move()
        self.lf.blitme()
        if self.lf.rect.x == self.screen.get_rect().right:
            self.lf.reset()
            self.smart_fish()

    def update_puffer(self):
        """update the puffers size and position"""
        self.puffer.blitme()
        self.puffer.change_puffer_size()
        self.puffer.move()
        sleep(0.05)
        if self.puffer.rect.x == self.screen.get_rect().left:
            self.puffer.reset()


    def update_sparkle(self):
        """if there is a sparkle, send it to the bubble"""
        if self.sparkleon:
            self.sparkle.blitme()
            if self.bubbles.rect.x < self.diver.rect.x:
                self.sparkle.pos = False
            self.sparkle.move()
            self._caught_bubbles()

    def update_sp_bubbles(self):
        """update the special bubbles"""
        #special bubbles are a powerup that returns a life to the player
        self.are_special_bubbles()
        self.add_special_bubbles()


    def are_special_bubbles(self):
        """use a timer to turn the special bubbles on and off"""
        time1 = int(time())
        #turn the bubbles on every 10 seconds for 3 seconds
        if (time1 - self.time0) % 10 == 3:
            self.spon = True
        if (time1 - self.time0) % 10 == 6:
            self.spon = False
            self.sp.reset()


    def add_special_bubbles(self):
        """if the special bubbles are on, print them"""
        if self.spon == True:
            self.sp.blitme()

    def smart_fish(self):
        """make the fish track the diver and swim towards them"""
        diver_position = [self.diver.rect.x, self.diver.rect.y]
        fish_position = [self.lf.rect.x, self.lf.rect.y]
        change_position = []
        for i in range(2):
            #find the x and y distance the fish needs to go to hit the diver
            change_position.append(diver_position[i]-fish_position[i])
        #find the angle the fish needs to go to hit the diver
        self.lf.theta = atan(change_position[1]/change_position[0])

    def check_mouse(self):
        """check if the mouse is over the bubbles, if so create a sparkle to shoot at it"""
        mouse = pygame.mouse.get_pos()
        if self.bubbles.rect.collidepoint(mouse):
            self.sparkleon = True
            self.sparkle = Sparkle(self)
            bubble_position = [self.bubbles.rect.x, self.bubbles.rect.y]
            sparkle_position = [self.sparkle.rect.x, self.sparkle.rect.y]
            change_position = []
            for i in range(2):
                change_position.append(bubble_position[i] - sparkle_position[i])
            #create the angle the sparkle will travel in in order to capture the bubble
            self.sparkle.theta = atan(change_position[1] / change_position[0])


    def _check_events(self):
        """respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #if the mouse was pressed, check if special bubbles were caught or the play button was clicked
                self._caught_sp(mouse)
                self.if_play(mouse)


    def _check_keydown_events(self, event):
        """respond to keypresses"""
        #if the up key is pressed, the diver jumps
        if event.key == pygame.K_UP:
            self.diver.jump()
            #gravity acts on the diver
            self.diver.gravity = True
        #if the q key is pressed, the game is over
        elif event.key == pygame.K_q:
            sys.exit()

    def if_play(self, mouse):
        """Start a new game when the player clicks the play button"""
        if self.play.rect.collidepoint(mouse):
            self.stats.reset_stats()
            self.lf.reset()
            self.puffer.reset()
            self.bubbles.reset()
            self.diver.restart_diver()
            self.stats.game_active =True


    def _check_fish_diver_collisions(self):
        """respond to fish and diver collisions"""
        #check for any fish that have hit the diver
        #if so lose a life
        if self.puffer.rect.colliderect(self.diver.rect) or self.lf.rect.colliderect(self.diver.rect):
            lost_life_sound = pygame.mixer.Sound("sounds/lostlife.wav")
            pygame.mixer.Sound.play(lost_life_sound)
            self.diver.restart_diver()
            self.puffer.reset()
            self.lf.reset()
            self.smart_fish()
            self.stats.livesleft -= 1

    def _caught_bubbles(self):
        """respond to bubble sparkle collisions"""
        #check if sparkle captured bubbles
        #if so increase score
        if self.sparkle.rect.colliderect(self.bubbles.rect):
            points_sound = pygame.mixer.Sound("sounds/sparkle.wav")
            pygame.mixer.Sound.play(points_sound)
            self.sparkleon = False
            self.stats.score += 10

            self.bubbles.reset()

    def _caught_sp(self,mouse):
        """respond to sparkle special bubbles collisions"""
        # check if sparkle hit special bubbles
        # if so, regain a life
        if self.sp.rect.collidepoint(mouse):
            self.spon = False
            self.sp.reset()
            self.stats.livesleft += 1



    def new_level(self):
        """increase the difficulty every time the score hits a new multiple of 100"""
        if self.stats.score != 0 and self.stats.score % 100 == 0:
            self.stats.score = self.stats.score + 10
            self.puffer.speed += 1
            self.lf.speed += 1
            self.puffer.reset()
            self.lf.reset()

    def instructions_screen(self):
        """print the instructions to the screen"""
        self.image2 = pygame.image.load('images/sand.png')
        self.image2 = pygame.transform.scale(self.image2, (1200, 600))
        self.screen.blit(self.image2, (0, 0))
        font = pygame.font.SysFont('arial', 50)
        img = font.render(f"Instructions: ", True, [200, 0, 100])
        self.screen.blit(img, (100, 100))
        font = pygame.font.SysFont('arial', 25)
        img = font.render(f"You are the diver", True, [200, 0, 100])
        self.screen.blit(img, (150, 175))
        img = font.render(f"Your goal is to avoid the fish - use the up arrow to jump out of the way", True, [200, 0, 100])
        self.screen.blit(img, (150, 250))
        img = font.render(f"To gain points, shoot pink bubbles", True, [200, 0, 100])
        self.screen.blit(img, (150, 325))
        img = font.render(f"Put your mouse over the bubbles to generate a sparkle, and move it off to shoot the sparkle at the bubbles", True, [200, 0, 100])
        self.screen.blit(img, (150, 400))
        self.diver.instruction_screen()
        self.bubbles.instruction_screen()
        self.puffer.instruction_screen()
        self.lf.instruction_screen()
        self.sparkle = Sparkle(self)
        self.sparkle.instruction_screen()


    def high_score(self):
        """update the high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score

    def display_high_score(self):
        """show the current high score on the screen"""
        self.high_score()
        font = pygame.font.SysFont('arial', 20)
        img = font.render(f"High Score: {self.stats.high_score}", True, [200, 0, 100])
        self.screen.blit(img, (20, 50))


    def update_score(self):
        """display the current score on the screen"""
        font = pygame.font.SysFont('arial', 20)
        img = font.render(f"Score: {self.stats.score}", True, [200, 0, 100])
        self.screen.blit(img, (20, 20))

    def update_lives(self):
        """update the number of lives the user has remaining"""
        self._check_fish_diver_collisions()
        x_value = 0
        #if no lives are left, the game is over
        if self.stats.livesleft == 0:
            self.stats.game_active = False
            self.lf.speed = 1
            self.puffer.reset_speed()
        #print small blue fish to show the number of lives remaining
        for i in range(self.stats.livesleft):
            self.l.rect.x = self.screen.get_width() - 75 - 50 * i
            x_value +=1
            self.l.blitme()
        #print fish skeletons to show the number of lives lost
        lost_lives = self.settings.lives - self.stats.livesleft
        for i in range(lost_lives):
            self.d.rect.x = self.screen.get_width() -75 -50 *x_value - 50 * i
            self.d.blitme()

if __name__ == '__main__':
    # make a game instance, and run the game
    uts = UnderTheSea()
    uts.run_game()
