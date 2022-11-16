import pygame


class Intro():
    def __init__(self):
        img = font.render(f"Score: {score}", True, (255,0,0))
        screen.blit(img, (20,20))
