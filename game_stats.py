

class GameStats:
    
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        # Start Game in inactive state
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.game_settings.ship_limit
        self.score = 0

