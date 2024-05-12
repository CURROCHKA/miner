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
        self.button_active = True
        self.who = ''

