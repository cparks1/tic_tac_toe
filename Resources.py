import pygame
from ResourceExceptions import InvalidCellSize


class Resources:
    def __init__(self):
        self.sprites = Sprites()
        self.colors = Colors()


class Sprites:
    def __init__(self):
        self.naught = pygame.image.load('resources/naught.png')
        self.draught = pygame.image.load('resources/draught.png')
        self.empty = pygame.image.load('resources/empty.png')
        self.cell = pygame.image.load('resources/cell.png')

        self.cell_sz = self.cell.get_size()
        if self.cell_sz[0] != self.cell_sz[1]:
            raise InvalidCellSize("Cell size must be rectangular. Cell width: %d, cell height: %d." % (self.cell_sz[0], self.cell_sz[1]))
        else:
            self.cell_sz = self.cell_sz[0]


class Colors:
    def __init__(self):
        self.White = (0, 0, 0)
        self.Black = (255, 255, 255)

        self.Red = (255, 0, 0)
        self.Green = (0, 255, 0)
        self.Blue = (0, 0, 255)

        self.Cyan = (0, 255, 255)
        self.Purple = (255, 0, 255)
        self.Yellow = (255, 255, 0)
