import sys
import pygame as pg
import game_functions as gf

from settings import Settings
from button import Button
from scores_button import ScoreButton
from game_stats import GameStats
from scoreboard import Scoreboard
from sound import Sound

from pygame.sprite import Group
from ship import Ship
from UFO import UFO

import time


class Game:
    def __init__(self):
        pg.init()

        # Text to show the game title
        self.game_title_font = pg.font.SysFont("monospace", 52)
        self.game_title = self.game_title_font.render("ALIEN INVASION", 1, (255, 255, 0))

        # Point label font
        self.point_label_font = pg.font.SysFont("monospace", 22)

        # Alien one and label to show on start screen
        self.alien_one = pg.image.load('images/Alien Types/Alien 1-1.png')
        self.alien_one = pg.transform.scale(self.alien_one, (150, 150))
        self.alien_one_label = self.point_label_font.render("50 pts.", 1, (255, 255, 255))

        # Alien two and label to show on start screen
        self.alien_two = pg.image.load('images/Alien Types/Alien 2-1.png')
        self.alien_two = pg.transform.scale(self.alien_two, (150, 150))
        self.alien_two_label = self.point_label_font.render("50 pts.", 1, (255, 255, 255))

        # Alien three and label to show on start screen
        self.alien_three = pg.image.load('images/Alien Types/Alien 3-1.png')
        self.alien_three = pg.transform.scale(self.alien_three, (150, 150))
        self.alien_three_label = self.point_label_font.render("50 pts.", 1, (255, 255, 255))

        # UFO and label to show on start screen
        self.ufo = pg.image.load('images/UFO/UFO.png')
        self.ufo = pg.transform.scale(self.ufo, (150, 150))
        self.ufo_label = self.point_label_font.render("???", 1, (255, 255, 255))

        self.play()

    def play(self):
        # pg.init()

        ai_settings = Settings()
        screen = pg.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
        pg.display.set_caption(ai_settings.title)

        # Text to show the game title
        self.game_title_font = pg.font.SysFont("monospace", 72)
        self.game_title = self.game_title_font.render("ALIEN INVASION", 1, (255, 255, 0))

        play_button = Button(ai_settings, screen, "Play")
        score_button = ScoreButton(ai_settings, screen, "High Score")

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
        aliens_list = []
        timer = [pg.time.get_ticks()]
        # blockers = Group()
        allBlockers = Group(gf.make_blockers(screen, 0), gf.make_blockers(screen, 1), gf.make_blockers(screen, 2), gf.make_blockers(screen, 3))
        UFO_object = UFO(ai_settings=ai_settings, screen=screen)

        gf.create_fleet(ai_settings=ai_settings, screen=screen, ships=ships, aliens=aliens)
        # gf.create_blockers(ai_settings=ai_settings, screen=screen, blockers=blockers)
        screen.fill(ai_settings.bg_color)
        while True:
            gf.check_events(ai_settings=ai_settings, screen=screen, play_button=play_button, scores_button=score_button,
                            stats=stats, sb=sb, sound=sound,
                            ships=ships, aliens=aliens, bullets=bullets)
            if stats.game_active:
                gf.update_ships(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, sound=sound,
                                ships=ships, aliens=aliens, bullets=bullets,  alien_bullets=alien_bullets)
                gf.update_aliens(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, sound=sound,
                                 ships=ships, aliens=aliens, bullets=bullets, alien_bullets=alien_bullets, timer=timer,
                                 aliens_list=aliens_list)
                gf.update_bullets(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, sound=sound,
                                  ships=ships, aliens=aliens, bullets=bullets)
                gf.update_alien_bullets(ai_settings=ai_settings, ships=ships, alien_bullets=alien_bullets)
                gf.update_UFO(screen=screen, UFO_object=UFO_object)
                # gf.update_blockers(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, sound=sound, ships=ships, aliens=aliens, bullets=bullets,  alien_bullets=alien_bullets, blockers=blockers)
                allBlockers.update(screen)
            else:
                screen.blit(self.game_title, (300, 100))
                screen.blit(self.alien_one, (200, 250))
                screen.blit(self.alien_one_label, (235, 380))
                screen.blit(self.alien_two, (400, 250))
                screen.blit(self.alien_two_label, (435, 380))
                screen.blit(self.alien_three, (600, 250))
                screen.blit(self.alien_three_label, (635, 380))
                screen.blit(self.ufo, (800, 220))
                screen.blit(self.ufo_label, (852, 380))

            gf.update_screen(ai_settings=ai_settings, screen=screen,
                             play_button=play_button, score_button=score_button, stats=stats, sb=sb, sound=sound,
                             ships=ships, aliens=aliens, bullets=bullets, alien_bullets=alien_bullets, UFO_object=UFO_object)


def main():
    g = Game()
    # g.play()


if __name__ == '__main__':
    main()
