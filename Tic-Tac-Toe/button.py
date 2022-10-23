import pygame.font
from settings import Settings


class Button:
    """Характеристики всех кнопок."""
    def __init__(self, t_game, name, rect):
        self.name = name
        self.settings = Settings()
        self.who = None
        self.status = True
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.button_color = self.settings.button_color
        self.rect = pygame.Rect(rect)
        self.button = self.settings.button

    def draw_button(self):
        self.button.fill(self.button_color)
        self.screen.blit(self.button, self.rect)
