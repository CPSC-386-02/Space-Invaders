import pygame as pg


class Sound:
    def __init__(self):
        pg.mixer.init()
        pg.mixer.music.load('sound/21 Guns.mp3')
        pg.mixer.music.set_volume(0.5)

        self.bullet_sound = pg.mixer.Sound('sound/Pew.mp3')
        pg.mixer.Sound.set_volume(self.bullet_sound, 0.22)

        self.explosion_sound = pg.mixer.Sound('sound/Pop.mp3')
        pg.mixer.Sound.set_volume(self.explosion_sound, 0.22)

        self.playing_bg = None
        self.play()
        self.pause_bg()

    def pause_bg(self):
        self.playing_bg = False
        pg.mixer.music.pause()

    def unpause_bg(self):
        self.playing_bg = True
        pg.mixer.music.unpause()

    def play(self):
        self.playing_bg = True
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        self.playing_bg = False
        pg.mixer.music.stop()

    def shoot_bullet(self):
        pg.mixer.Sound.play(self.bullet_sound)

    def alien_hit(self):
        pg.mixer.Sound.play(self.explosion_sound)
