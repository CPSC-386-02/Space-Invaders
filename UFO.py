import pygame as pg
from timer import Timer
from pygame.sprite import Sprite


class UFO(Sprite):
    ship = [pg.image.load('images/Ship/Ship.png')]
    ship_exploded = [pg.image.load('images/Ship Explosion/Ship explosion ' + str(i) + '.png') for i in range(2, 14)]
    timer_ship = Timer(ship, 400)
    timer_explode = Timer(ship_exploded, 30, True)

    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.appear = None
        self.hit = None

        self.image = pg.image.load('images/UFO/UFO.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height + 25

        self.direction = 1

        self.x = float(self.rect.x)

    def initialize(self, x, direction):
        self.rect.x = x
        self.x = float(self.rect.x)
        self.direction = direction

    def reset(self):
        self.appear = False
        self.rect.x = self.rect.width
        self.x = float(self.rect.x)

    def UF0_check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            self.reset()
        elif self.rect.left <= 0:
            self.reset()

    def update(self):
        if self.appear:
            self.x += 1 * self.direction
            self.rect.x = self.x

    def draw_UFO(self):
        self.screen.blit(self.image, self.rect)
