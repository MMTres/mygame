import pygame.font

class PlayButton:
    def __init__(self, uts):
        """initialize attributes of play button"""
        self.screen = uts.screen
        self.screen_rect = self.screen.get_rect()

        #set up the buttons size and properties
        self.width = 100
        self.height = 100
        self.color = (255,255,255)
        self.text_color = (200, 0, 100)
        self.font = pygame.font.SysFont(None, 50)

        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.x = 550
        self.rect.y = 450

        self.make_button_text()

    def make_button_text(self):
        """make the button into a rendered image"""
        self.image = self.font.render("Play", True, self.text_color, self.color)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

    def draw_button(self):
        """draw blank button and add the text"""
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.image, self.image_rect)