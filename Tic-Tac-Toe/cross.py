import pygame


class Cross:
    """Крестик"""

    def __init__(self, t_game):
        self.screen = t_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('image/cross.png')
        self.rect = self.image.get_rect()

    def update(self):
        self.screen.blit(self.image, self.rect)
