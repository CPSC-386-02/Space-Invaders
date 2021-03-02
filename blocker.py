import pygame as pg
from pygame.surface import Surface

import game
from pygame.sprite import Sprite


class Blocker(Sprite):

    def __init__(self, size, color, row, column):
        Sprite.__init__(self)
        self.height = size
        self.width = size
        self.color = color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        print(self.rect)
        self.row = row
        self.column = column

    def update(self, screen, keys, *args):
        # game.screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect)
