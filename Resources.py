import pygame


class Resources:
    def __init__(self):
        self.sprites = Sprites()


class Sprites:
    def __init__(self):
        self.naught = pygame.image.load('resources/naught.png')
        self.draught = pygame.image.load('resources/draught.png')
        self.empty = pygame.image.load('resources/empty.png')
