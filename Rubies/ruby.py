import pygame
from random import choice


class Ruby:
    def __init__(self, rubies_game, color: str):
        super().__init__()
        self.rg = rubies_game
        self.screen = self.rg.screen
        self.color = color
        self.image = pygame.image.load(f'images/{self.color}.png')
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.id = None

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update_pos(self, x, y):
        self.rect.x, self.rect.y = self.rect.x + x, self.rect.y + y

    def change_color(self, color):
        self.color = color
        self.image = pygame.image.load(f'images/{self.color}.png')
