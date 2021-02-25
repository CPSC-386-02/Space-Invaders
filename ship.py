import pygame as pg
from pygame.sprite import Sprite
from timer import Timer


class Ship(Sprite):
    ship_exploded = [pg.image.load('images/Ship explosion ' + str(i) + '.png') for i in range(2, 12)]
    timer_explode = Timer(ship_exploded, 10, True)

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.dead = False
        self.really_dead = False
        self.timer_switched = False
        self.timer = Ship.timer_explode

        self.image = pg.image.load('images/Ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.dead:
            self.timer_switched = True
            if self.timer.frame_index() == len(Ship.ship_exploded) - 1:
                self.dead = False
                self.really_dead = True
                self.timer.reset()

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed

        self.rect.centerx = self.center

    def draw_ship(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
