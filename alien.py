import pygame as pg
from timer import Timer
from pygame.sprite import Sprite


class Alien(Sprite):
    alien_images = [[pg.image.load('images/Alien ' + str(number) + '-' + str(i) + '.png') for i in range(1, 4)] for number in range(1, 4)]
    alien_exploded = [pg.image.load('images/Alien explosion 1-' + str(i) + '.png') for i in range(1, 5)]
    timers = []
    for i in range(3):
        timers.append(Timer(alien_images[i], 400))

    timer_explode = Timer(alien_exploded, 10, True)

    def __init__(self, ai_settings, screen, number=0):
        super(Alien, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.number = number
        self.dead = False
        self.really_dead = False
        self.timer_switched = False

        self.timer = Alien.timers[number]
        self.rect = self.timer.imagerect().get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        if self.dead and not self.timer_switched:
            self.timer = Alien.timer_explode
            self.timer_switched = True
        elif self.dead and self.timer_switched:
            if self.timer_explode.frame_index() == len(Alien.alien_exploded) - 1:
                self.dead = False
                self.really_dead = True
                self.timer_switched = False
                self.timer.reset()
        self.x += self.ai_settings.alien_speed * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def draw_alien(self):
        alien = self.timer.imagerect()
        rect = alien.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(alien, rect)
