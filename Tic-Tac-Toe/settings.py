import pygame


class Settings:
    """Основные настройки игры."""

    def __init__(self):
        # Настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_color = (255, 255, 255)
        # Настройки кнопок
        self.button = pygame.Surface((125, 125))
        self.button_color = (255, 255, 255)

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.topleft_active = True
        self.topleft_who = ''

        self.center_active = True
        self.center_who = ''

        self.topright_active = True
        self.topright_who = ''

        self.top_active = True
        self.top_who = ''

        self.left_active = True
        self.left_who = ''

        self.bottomleft_active = True
        self.bottomleft_who = ''

        self.bottom_active = True
        self.bottom_who = ''

        self.bottomright_active = True
        self.bottomright_who = ''

        self.right_active = True
        self.right_who = ''
