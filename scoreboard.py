import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("None", 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

        self.UFO_score_image = None
        self.UFO_score_rect = None

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ship(self):
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_UFO_score(self, UFO_object, score):
        UFO_object.hit = True
        UFO_score_str = str(score)
        self.UFO_score_image = self.font.render(UFO_score_str, True, self.text_color, self.ai_settings.bg_color)
        self.UFO_score_rect = self.UFO_score_image.get_rect()
        self.UFO_score_rect.x = UFO_object.rect.x
        self.UFO_score_rect.y = UFO_object.rect.y

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def show_UFO_score(self):
        self.screen.blit(self.UFO_score_image, self.UFO_score_rect)
