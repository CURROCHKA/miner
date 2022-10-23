import pygame.font
from settings import Settings


class Buttons:
    """Характеристики всех кнопок."""
    def __init__(self, t_game):
        self.settings = Settings()
        self.who = t_game.who
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        self.button_color = self.settings.button_color

        # Topleft button
        self.topleft_button = self.settings.button
        self.topleft_rect = pygame.Rect(446, 205, 125, 125)

        # Center button
        self.center_button = self.settings.button
        self.center_rect = pygame.Rect(577, 336, 125, 125)

        # Topright button
        self.topright_button = self.settings.button
        self.topright_rect = pygame.Rect(705, 205, 125, 125)

        # Top button
        self.top_button = self.settings.button
        self.top_rect = pygame.Rect(577, 205, 125, 125)

        # Left button
        self.left_button = self.settings.button
        self.left_rect = pygame.Rect(446, 336, 125, 125)

        # Bottomleft button
        self.bottomleft_button = self.settings.button
        self.bottomleft_rect = pygame.Rect(446, 466, 125, 125)

        # Bottom button
        self.bottom_button = self.settings.button
        self.bottom_rect = pygame.Rect(577, 466, 125, 125)

        # Bottomright button
        self.bottomright_button = self.settings.button
        self.bottomright_rect = pygame.Rect(705, 466, 125, 125)

        # Right button
        self.right_button = self.settings.button
        self.right_rect = pygame.Rect(705, 336, 125, 125)

    def draw_button(self):
        # Topleft button
        self.topleft_button.fill(self.button_color)
        self.screen.blit(self.topleft_button, self.topleft_rect)

        # Center button
        self.center_button.fill(self.button_color)
        self.screen.blit(self.center_button, self.center_rect)

        # Topright button
        self.topright_button.fill(self.button_color)
        self.screen.blit(self.topright_button, self.topright_rect)

        # Top button
        self.top_button.fill(self.button_color)
        self.screen.blit(self.top_button, self.top_rect)

        # Left button
        self.left_button.fill(self.button_color)
        self.screen.blit(self.left_button, self.left_rect)

        # Buttomleft button
        self.bottomleft_button.fill(self.button_color)
        self.screen.blit(self.bottomleft_button, self.bottomleft_rect)

        # Bottom button
        self.bottom_button.fill(self.button_color)
        self.screen.blit(self.bottom_button, self.bottom_rect)

        # Bottomright button
        self.bottomright_button.fill(self.button_color)
        self.screen.blit(self.bottomright_button, self.bottomright_rect)

        # Right button
        self.right_button.fill(self.button_color)
        self.screen.blit(self.right_button, self.right_rect)

