import sys

import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group


def run_game():
    # Initiate game and create a screen object.
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))

    # Make Ship
    ship = Ship(screen, game_settings)
    alien = Alien(game_settings, screen)
    pygame.display.set_caption("MAL MAL MAL MAL")

    # Make the Play Button
    play_button = Button(game_settings, screen, "Play")
    # Make a Group to store bullets in.
    bullets = Group()
    # Make a Group of alien fleet
    aliens = Group()
    gf.create_fleet(game_settings, screen, aliens, ship)
    stats = GameStats(game_settings)
    play_button = Button(game_settings, screen, "Play")

    sb = Scoreboard(game_settings,screen,stats)


    while True:
        # Watch for keyboard event and mouse event
        gf.check_events(game_settings, screen, ship, bullets, stats, play_button, aliens)

        if stats.game_active:
            ship.update()
            gf.update_bullets(game_settings, screen, bullets, aliens, ship, stats, sb)
            gf.update_aliens(game_settings, screen, aliens, ship, stats, bullets)

        gf.update_screen(game_settings, screen, ship, bullets, aliens, play_button, stats,sb)


run_game()
