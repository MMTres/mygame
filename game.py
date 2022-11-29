import pygame
import sys
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
        self.life = Life(self)
        self.death = LostLife(self)
        self.bubbles = Bubbles(self)
        self.sp = SpecialBubbles(self)

        #initialize the game statistics
        self.stats = Stats(self)

        #create the play button
        self.play = PlayButton(self)

    def run_game(self):
        while True:

            self.reset_screen()
            self._check_events()
            if self.stats.game_active == True:

                self.update_sprites()
                self.update_stats()
                self.check_mouse()

            else:
                #show the instructions on the screen
                self.instructions_screen()
                self.play.draw_button()

            pygame.display.flip()

    def reset_screen(self):
        """reset the screen's background"""
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.image, (0, 0))

    def update_sprites(self):
        """update the sprites shown on the screen"""
        self.puffer.update_puffer()
        self.lf.update_little_fish()
        self.diver.update_diver()
        self.update_sparkle()
        self.bubbles.draw()
        self.sp.update_sp_bubbles()

    def update_stats(self):
        """update the statistics shown on the screen"""
        self.stats.update_score()
        self.stats.display_high_score()
        self.update_lives()
        self.new_level()

    def update_sparkle(self):
        """if there is a sparkle, send it to the bubble"""
        if self.settings.sparkleon:
            self.sparkle.draw()
            #if the bubble is in front of the diver, set the sparkle to travel in the positive direction
            if self.bubbles.rect.x < self.diver.rect.x:
                self.sparkle.pos = False
            self.sparkle.move()
            #check if the sparkle has caught the bubble
            self.caught_bubbles()

    def check_mouse(self):
        """check if the mouse is over the bubbles, if so create a sparkle to shoot at it"""
        #mouse master code achievement
        mouse = pygame.mouse.get_pos()
        if self.bubbles.rect.collidepoint(mouse):
            self.settings.sparkleon = True
            self.sparkle = Sparkle(self)
            bubble_position = [self.bubbles.rect.x, self.bubbles.rect.y]
            sparkle_position = [self.sparkle.rect.x, self.sparkle.rect.y]
            change_position = []
            #find the change in x and y that the sparkle must travel
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
                self._caught_special_bubbles(mouse)
                self.if_play(mouse)

    def _check_keydown_events(self, event):
        """respond to keypresses"""
        #keyboard king code achievement
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
            #play a sound when a life is lost
            lost_life_sound = pygame.mixer.Sound("sounds/lostlife.wav")
            pygame.mixer.Sound.play(lost_life_sound)
            #reset the fish and diver when a life is lost
            self.diver.restart_diver()
            self.puffer.reset()
            self.lf.reset()
            self.stats.livesleft -= 1

    def caught_bubbles(self):
        """respond to bubble sparkle collisions"""
        #check if sparkle captured bubbles
        #if so increase score
        #sound blaster code achievement
        if self.sparkle.rect.colliderect(self.bubbles.rect):
            points_sound = pygame.mixer.Sound("sounds/sparkle.wav")
            pygame.mixer.Sound.play(points_sound)
            self.settings.sparkleon = False
            self.stats.score += 10
            self.bubbles.reset()

    def _caught_special_bubbles(self,mouse):
        """respond to sparkle special bubbles collisions"""
        # check if sparkle hit special bubbles
        # if so, regain a life
        #healthy eater code achievement
        if self.sp.rect.collidepoint(mouse):
            self.settings.special_on = False
            self.sp.reset()
            self.stats.livesleft += 1

    def new_level(self):
        """increase the difficulty every time the score hits a new multiple of 100"""
        #level up code achievement
        #update the level displayed on the screen
        font = pygame.font.SysFont('arial', 25)
        img = font.render(f"Level: {self.puffer.speed} ", True, [50, 0, 200])
        self.screen.blit(img, (1100, 550))
        if self.stats.score != 0 and self.stats.score % 100 == 0:
            #player gets a 10 point bonus when they hit a new level
            self.stats.score = self.stats.score + 10
            self.puffer.speed += 1
            self.lf.speed += 1
            self.puffer.reset()
            self.lf.reset()

    def instructions_screen(self):
        """print the instructions to the screen"""
        #shifting screens code achievement
        #create new background with beach image
        self.image2 = pygame.image.load('images/sand.png')
        self.image2 = pygame.transform.scale(self.image2, (1200, 600))
        self.screen.blit(self.image2, (0, 0))
        #print instructions with pictures of the sprites
        font = pygame.font.SysFont('arial', 50)
        img = font.render(f"Instructions: ", True, [200, 0, 100])
        self.screen.blit(img, (75, 25))
        font = pygame.font.SysFont('arial', 25)
        img = font.render(f"You are the diver", True, [200, 0, 100])
        self.screen.blit(img, (100, 100))
        img = font.render(f"Your goal is to avoid the fish - use the up arrow to jump out of the way", True, [200, 0, 100])
        self.screen.blit(img, (100, 175))
        img = font.render(f"To gain points, shoot pink bubbles", True, [200, 0, 100])
        self.screen.blit(img, (100, 250))
        img = font.render(f"Put your mouse over the bubbles to generate a sparkle, and move it off to shoot the sparkle at the bubbles", True, [200, 0, 100])
        self.screen.blit(img, (100, 325))
        img = font.render(f"To regain a life, click the green bubbles that appear briefly on the screen", True, [200, 0, 100])
        self.screen.blit(img, (100, 400))
        img = font.render(f"The fish will get faster as you go, watch out!", True,[200, 0, 100])
        self.screen.blit(img, (100, 475))
        self.diver.instruction_screen()
        self.bubbles.instruction_screen()
        self.puffer.instruction_screen()
        self.lf.instruction_screen()
        self.sparkle = Sparkle(self)
        self.sparkle.instruction_screen()
        self.sp.instruction_screen()

    def update_lives(self):
        """update the number of lives the user has remaining and display on the screen"""
        #looking weak code achievement
        self._check_fish_diver_collisions()
        #keep count of how many live fish are shown to know how many dead fish to show
        count = 0
        #if no lives are left, the game is over
        if self.stats.livesleft == 0:
            self.stats.game_active = False
            self.lf.speed = 1
            self.puffer.reset_speed()
        #print small blue fish to show the number of lives remaining
        for i in range(self.stats.livesleft):
            self.life.rect.x = self.screen.get_width() - 75 - 50 * i
            count +=1
            self.life.draw()
        #print fish skeletons to show the number of lives lost
        lost_lives = self.settings.lives - self.stats.livesleft
        for i in range(lost_lives):
            self.death.rect.x = self.screen.get_width() -75 -50 *count - 50 * i
            self.death.draw()

if __name__ == '__main__':
    # make a game instance, and run the game
    uts = UnderTheSea()
    uts.run_game()
