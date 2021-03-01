import random
import sys
import pygame as pg
import pickle

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


def check_events(ai_settings, screen, play_button, scores_button, stats, sb, sound, ships, aliens, bullets):
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
            check_scores_button(screen, scores_button, stats, mouse_x, mouse_y)


def update_screen(ai_settings, screen, play_button, score_button, stats, sb, sound, ships, aliens, bullets,
                  alien_bullets, UFOs, timer_score_display):
    if stats.game_active:
        screen.fill(ai_settings.bg_color)
        for ship in ships:
            ship.draw_ship()
        for alien in aliens.sprites():
            alien.draw_alien()
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in alien_bullets.sprites():
            alien_bullet.draw_alien_bullet()
        for UFO_object in UFOs:
            if UFO_object.appear:
                UFO_object.draw_UFO()
            if UFO_object.hit:
                if (pg.time.get_ticks() - timer_score_display[0]) < 500:
                    sb.show_UFO_score()
                else:
                    UFO_object.hit = False
        sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
        score_button.draw_button()
        sound.pause_bg()
    else:
        if not sound.playing_bg:
            sound.unpause_bg()
    pg.display.flip()


########################################################################################################################


################################################### ALIENS FUNCTIONS ###################################################


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 1 * alien_width
    number_aliens_x = int(available_space_x / (1 * alien_width))
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
    alien.x = alien_width + 1 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 0.8 * alien.rect.height * row_number + 80
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


def check_aliens_bottom(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, UFOs):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, UFOs)
            break


def update_aliens(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, timer, aliens_list, UFOs):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    for ship in ships:
        if pg.sprite.spritecollideany(ship, aliens):
            ship_hit(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, UFOs)
    check_aliens_bottom(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, UFOs)
    aliens_list.clear()
    for alien in aliens:
        alien.update()
        aliens_list.append(alien)
        if alien.really_dead:
            aliens.remove(alien)
    alien_fire_bullets(ai_settings, screen, alien_bullets, timer, aliens_list)


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


############################################### ALIEN BULLETS FUNCTIONS ################################################


def alien_fire_bullets(ai_settings, screen, alien_bullets, timer, aliens_list):
    if (pg.time.get_ticks() - timer[0]) > 1000:
        alien = random.choice(aliens_list)
        new_bullet = Alien_Bullet(ai_settings, screen, alien)
        alien_bullets.add(new_bullet)
        timer.pop()
        timer.append(pg.time.get_ticks())


def check_bullet_ship_collisions(ships, alien_bullets):
    collisions = pg.sprite.groupcollide(alien_bullets, ships, True, False)
    if collisions:
        for ships in collisions.values():
            for ship in ships:
                ship.dead = True


def update_alien_bullets(ai_settings, ships, alien_bullets):
    alien_bullets.update()
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.bottom >= ai_settings.screen_height:
            alien_bullets.remove(alien_bullet)
    check_bullet_ship_collisions(ships, alien_bullets)


########################################################################################################################


#################################################### SHIP FUNCTIONS ####################################################


def update_ships(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, UFOs):
    ships.update()
    for ship in ships:
        if ship.really_dead:
            ship.really_dead = False
            ship_hit(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, UFOs)


def ship_hit(ai_settings, screen, stats, sb, sound, ships, aliens, bullets, alien_bullets, UFOs):
    if stats.ship_left > 1:
        stats.ship_left -= 1
        sb.prep_ship()
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        for UFO_object in UFOs:
            UFO_object.reset()
            UFO_object.hit = False

        create_fleet(ai_settings, screen, ships, aliens)
        for ship in ships:
            ship.center_ship()

        sleep(0.5)
    else:
        screen.fill(ai_settings.bg_color)
        stats.game_active = False
        sound.pause_bg()
        pg.mouse.set_visible(True)


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


def check_scores_button(screen, scores_button, stats, mouse_x, mouse_y):
    button_clicked = scores_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        high_score_font = pg.font.SysFont("monospace", 32)
        high_score_text = high_score_font.render("Current High Score: " + str(stats.high_score), True, (255, 255, 255))
        screen.blit(high_score_text, (360, 670))


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open('score.dat', 'wb') as file:
            pickle.dump(stats.high_score, file)


########################################################################################################################


def UFO_appear(screen, UFO_object):
    if random.randint(0, 600) == 1:
        UFO_object.appear = True
        if random.randint(1, 2) == 1:
            UFO_object.initialize(UFO_object.rect.width, 1)
        else:
            UFO_object.initialize(screen.get_rect().right - UFO_object.rect.width, -1)


def update_UFO(ai_settings, screen, stats, sb, sound, bullets, UFOs, timer_value_display):
    for UFO_object in UFOs:
        if not UFO_object.appear and not UFO_object.hit:
            UFO_appear(screen, UFO_object)
        UFO_object.update()
        UFO_object.UF0_check_edges()
    check_collisions_bullets_alien(ai_settings, stats, sb, sound, bullets, UFOs, timer_value_display)


def check_collisions_bullets_alien(ai_settings, stats, sb, sound, bullets, UFOs, timer_score_display):
    collisions = pg.sprite.groupcollide(bullets, UFOs, True, False)
    if collisions:
        for UFOs in collisions.values():
            score = ai_settings.UFO_score[random.randint(0, 2)]
            for UFO_object in UFOs:
                timer_score_display.pop()
                timer_score_display.append(pg.time.get_ticks())
                sb.prep_UFO_score(UFO_object, score)
                UFO_object.reset()
            stats.score += score
            sb.prep_score()
        check_high_score(stats, sb)
        sound.alien_hit()
