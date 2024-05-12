import pygame.font
from settings import Settings


class Button:
    """Характеристики всех кнопок."""
    def __init__(self, t_game, x, y, rect_w, rect_h):
        self.settings = Settings()
        self.screen = t_game.screen
        self.button_color = self.settings.button_color
        self.button_active = self.settings.button_active
        self.button = self.settings.button
        self.who = self.settings.who
        self.rect = pygame.Rect(x, y, rect_w, rect_h)

    def draw_button(self):
        self.button.fill(self.button_color)
        self.screen.blit(self.button, self.rect)
