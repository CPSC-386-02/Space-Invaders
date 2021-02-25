import random
import sys
import pygame as pg
import pickle
import time

from alien import Alien
from bullet import Bullet
from time import sleep
from alien_bullet import Alien_Bullet


################################################ CHECK EVENT FUNCTIONS #################################################
def check_key_down(event, ai_settings, screen, sound, ships, bullets):
    if event.key == pg.K_RIGHT:
        for ship in ships:
            ship.moving_right = True
    elif event.key == pg.K_LEFT:
        for ship in ships:
            ship.moving_left = True
    elif event.key == pg.K_SPACE:
        fire_bullets(ai_settings, screen, ships, bullets)
        sound.shoot_bullet()


def check_key_up(event, ships):
    if event.key == pg.K_RIGHT:
        for ship in ships:
            ship.moving_right = False
    elif event.key == pg.K_LEFT:
        for ship in ships:
            ship.moving_left = False


def check_events(ai_settings, screen, play_button, stats, sb, sound, ships, aliens, bullets):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            check_key_down(event, ai_settings, screen, sound, ships, bullets)
        elif event.type == pg.KEYUP:
            check_key_up(event, ships)
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(ai_settings, screen, play_button, stats, sb, ships, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen, play_button, stats, sb, sound, ships, aliens, bullets, alien_bullets):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for ship in ships:
        ship.draw_ship()
    for alien in aliens.sprites():
        alien.draw_alien()
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_alien_bullet()
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
        sound.pause_bg()
    else:
        if not sound.playing_bg:
            sound.unpause_bg()
    pg.display.flip()


########################################################################################################################


################################################### ALIENS FUNCTIONS ###################################################
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (1 * ship_height) - ship_height)
    number_rows = int(available_space_y / (1.8 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    if row_number == 2 or row_number == 3:
        alien = Alien(ai_settings, screen, 1)
    elif row_number == 4 or row_number == 5:
        alien = Alien(ai_settings, screen, 2)
    else:
        alien = Alien(ai_settings, screen, 0)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ships, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    for ship in ships:
        number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, sound, ships, aliens, bullets):
    if stats.ship_left > 1:
        stats.ship_left -= 1
        sb.prep_ship()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ships, aliens)
        for ship in ships:
            ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        sound.pause_bg()
        pg.mouse.set_visible(True)


def check_aliens_bottom(ai_settings,  screen, stats, sb, sound, ships, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, sound, ships, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, timer):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    alien_fire_bullets(ai_settings, screen, aliens, alien_bullets, timer)
    for ship in ships:
        if pg.sprite.spritecollideany(ship, aliens):
            ship_hit(ai_settings, screen, stats,  sb, sound, ships, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, sound, ships, aliens, bullets)
    for alien in aliens:
        alien.update()
        if alien.really_dead:
            aliens.remove(alien)


########################################################################################################################


################################################## BULLETS FUNCTIONS ###################################################
def fire_bullets(ai_settings, screen, ships, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        for ship in ships:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, sound, ships, aliens, bullets):
    collisions = pg.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                alien.dead = True
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
        sound.alien_hit()
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ships, aliens)


def update_bullets(ai_settings, screen, stats, sb, sound, ships, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, sound, ships, aliens, bullets)


########################################################################################################################


################################################## ALIEN BULLETS FUNCTIONS ###################################################
def alien_fire_bullets(ai_settings, screen, aliens, alien_bullets, timer):
    if (pg.time.get_ticks() - timer[0]) > 1000:
        for alien in aliens:
            new_bullet = Alien_Bullet(ai_settings, screen, alien)
            alien_bullets.add(new_bullet)
        timer.pop()
        timer.append(pg.time.get_ticks())


def check_bullet_ship_collisions(ai_settings, screen, stats, sb, sound, ships, aliens, alien_bullets):
    collisions = pg.sprite.groupcollide(alien_bullets, ships, True, False)
    if collisions:
        for ships in collisions.values():
            for ship in ships:
                ship.dead = True
        sound.alien_hit()


def update_alien_bullets(ai_settings, alien_bullets):
    alien_bullets.update()
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.bottom >= ai_settings.screen_height:
            alien_bullets.remove(alien_bullet)


def update_ships(ships):
    ships.update()
########################################################################################################################


############################################### OPENING SCREEN FUNCTIONS ###############################################
def check_play_button(ai_settings, screen, play_button, stats, sb, ships, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()

        pg.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ships, aliens)
        for ship in ships:
            ship.center_ship()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open('score.dat', 'wb') as file:
            pickle.dump(stats.high_score, file)
########################################################################################################################
