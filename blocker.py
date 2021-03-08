from pygame.surface import Surface
from pygame.sprite import Sprite


class Blocker(Sprite):

    def __init__(self, screen, size, color, row, column):
        Sprite.__init__(self)
        self.screen = screen
        self.height = size
        self.width = size
        self.color = color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column

    def draw_barrier(self):
        self.screen.blit(self.image, self.rect)
