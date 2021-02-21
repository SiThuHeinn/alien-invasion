import pygame

import sys

from bullet import Bullet
from alien import Alien
from time import sleep


def get_number_rows(game_settings, alien_height, ship_height):
    available_space_y = (game_settings.screen_height - (2 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows + 1


def get_number_aliens_x(game_settings, alien_width):
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(game_settings, screen, number_aliens_x, aliens, row_number):
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * number_aliens_x
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * (alien.rect.height - 40) * row_number - 40
    aliens.add(alien)


def create_fleet(game_settings, screen, aliens, ship):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, alien.rect.height, ship.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, alien_number, aliens, row_number)


def check_events(game_settings, screen, ship, bullets, stats, play_button, aliens):
    """Response to Keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            keydown_events(event, game_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, game_settings, screen)


def keyup_events(event, ship):
    """Respond to key press event"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def keydown_events(event, game_settings, screen, ship, bullets):
    """Respond to key release event"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Create a new bullet and add it to the bullets group.
        if len(bullets) < game_settings.bullet_allowed:
            new_bullet = Bullet(game_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()


def update_bullets(game_settings, screen, bullets, aliens, ship, stats, sb):
    bullets.update()
    # Get rid of bullets that has disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(game_settings, screen, ship, aliens, bullets, stats, sb)


def check_bullet_alien_collision(game_settings, screen, ship, aliens, bullets, stats, sb):
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            sb.prep_score()

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet
        bullets.empty()
        game_settings.increase_speed()
        create_fleet(game_settings, screen, aliens, ship)


def check_fleet_edges(game_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def update_aliens(game_settings, screen, aliens, ship, stats, bullets):
    check_fleet_edges(game_settings, aliens)
    aliens.update()
    # Check Alien Ship Collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, ship, aliens, bullets)

    # Check Alien hit Bottom
    check_aliens_bottom(game_settings, screen, stats, ship, aliens, bullets)


def ship_hit(game_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # Clear the list of Aliens and Bullets
        aliens.empty()
        bullets.empty()

        create_fleet(game_settings, screen, aliens, ship)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(game_settings, screen, stats, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, stats, screen, ship, aliens, bullets)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, game_settings, screen):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        # Reset the Game
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            """Hide Mouse Cursor"""
            game_settings.initialize_dynamic_settings()
            pygame.mouse.set_cursor(False)
            stats.reset_stats()
            stats.game_active = True

            aliens.empty()
            bullets.empty()

            create_fleet(game_settings, screen, aliens, ship)
            ship.center_ship()


def update_screen(settings, screen, ship, bullets, aliens, play_button, stats,sb):
    screen.fill(settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Show the Score
    sb.show_score()
    # Draw Play Button
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible 
    pygame.display.flip()
