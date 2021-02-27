import pygame as pg
from pygame.sprite import Sprite


class Alien_Bullet(Sprite):

    def __init__(self, ai_settings, screen, alien):
        super(Alien_Bullet, self).__init__()
        self.screen = screen

        self.rect = pg.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_length)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw_alien_bullet(self):
        pg.draw.rect(self.screen, self.color, self.rect)
