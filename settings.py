class Settings:

    # A Class to store game Settings.
    def __init__(self):
        """Initial Game Settings"""
        # Screen Settings
        self.screen_width = 1300
        self.screen_height = 720
        self.bg_color = (10, 10, 10)

        # Bullet Settings
        self.bullet_speed_factor = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 200, 0)
        self.bullet_allowed = 50

        # Alien Settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Ship Settings
        self.ship_speed_factor = 1.0
        self.ship_limit = 3

        """Game Speed up"""
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Level Up Speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
