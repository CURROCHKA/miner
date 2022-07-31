import pygame


class Ruby:
    def __init__(self, rubies_game, color: str):
        self.screen = rubies_game.screen
        self.color = color
        self.image = pygame.image.load(f'images/{self.color}.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)
