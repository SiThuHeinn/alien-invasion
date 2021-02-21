import pygame.font


class Scoreboard:
    """A Class to update scoring information"""

    def __init__(self, game_settings, screen, stats):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats

        """Score Font Settings"""
        self.text_color = (102, 178, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.game_settings.bg_color)

        """Display the Score at Top Right of the screen"""
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)



