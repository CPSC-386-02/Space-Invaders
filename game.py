import sys
import pygame as pg
import game_functions as gf

from settings import Settings
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from sound import Sound

from pygame.sprite import Group
from ship import Ship

import time

class Game:
    def __init__(self): pass

    def play(self):
        pg.init()

        ai_settings = Settings()
        screen = pg.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
        pg.display.set_caption(ai_settings.title)

        play_button = Button(ai_settings, screen, "Play")

        stats = GameStats(ai_settings=ai_settings)
        sb = Scoreboard(ai_settings=ai_settings, screen=screen, stats=stats)

        sound = Sound()
        sound.play()
        sound.pause_bg()

        ship = Ship(ai_settings=ai_settings, screen=screen)

        ships = Group()
        ships.add(ship)
        aliens = Group()
        bullets = Group()
        alien_bullets = Group()

        timer = []
        timer.append(pg.time.get_ticks())

        gf.create_fleet(ai_settings=ai_settings, screen=screen, ships=ships, aliens=aliens)

        while True:
            gf.check_events(ai_settings=ai_settings, screen=screen, play_button=play_button, stats=stats, sb=sb, sound=sound,
                            ships=ships, aliens=aliens, bullets=bullets)
            if stats.game_active:
                gf.update_ships(ships=ships)
                gf.update_aliens(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, sound=sound,
                                 ships=ships, aliens=aliens, bullets=bullets, alien_bullets=alien_bullets, timer=timer)
                gf.update_bullets(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, sound=sound,
                                  ships=ships, aliens=aliens, bullets=bullets)
                gf.update_alien_bullets(ai_settings, alien_bullets)
            gf.update_screen(ai_settings=ai_settings, screen=screen, play_button=play_button, stats=stats, sb=sb, sound=sound,
                             ships=ships, aliens=aliens, bullets=bullets, alien_bullets=alien_bullets)


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
