import sys
import pygame as pg
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class Game:
    def __init__(self): pass

    def play(self):
        pg.init()
        ai_settings = Settings()
        screen = pg.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
        pg.display.set_caption(ai_settings.title)

        play_button = Button(ai_settings, screen, "Play")

        stats = GameStats(ai_settings=ai_settings)
        sb = Scoreboard(ai_settings, screen, stats)

        ship = Ship(ai_settings=ai_settings, screen=screen)

        bullets = Group()
        aliens = Group()

        gf.create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens)

        while True:
            gf.check_events(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, play_button=play_button, ship=ship,aliens=aliens, bullets=bullets)
            if stats.game_active:
                ship.update()
                gf.update_bullets(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, bullets=bullets, aliens=aliens)
                gf.update_aliens(ai_settings=ai_settings, stats=stats, screen=screen, sb=sb,ship=ship, bullets=bullets, aliens=aliens)
            gf.update_screen(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, bullets=bullets, aliens=aliens, play_button=play_button)


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
