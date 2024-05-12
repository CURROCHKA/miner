import pygame


class Field:
    """Поле игры"""

    def __init__(self, t_game):
        # Главный экран
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()
        # Изображение поля
        self.image = pygame.image.load('../image/field.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        # Позиция поля

    def update(self):
        self.screen.blit(self.image, self.rect)

