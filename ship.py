import pygame


class Ship:
    def __init__(self, screen, game_settings):
        self.screen = screen

        # Load the image 

        self.image = pygame.image.load('images/middlefinger.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # game settings
        self.game_settings = game_settings

        # Position the Ship at Bottom | Centre
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 20

        # Store a decimal value for ship's center
        self.center = float(self.rect.centerx)

        # Movement Flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's center value, not the rect.

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        # Update position 
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        print("Image Rect   :   " + str(self.rect))
        print("Screen Rect  :   " + str(self.screen_rect))
        print("Image Position   :   " + str(self.rect.centerx) + ":" + str(self.rect.bottom))
        print("Image Rect Rign  :   " + str(self.rect.right))
