import pygame


class Fruit:
    def __init__(self, coord: tuple, size: tuple, color: tuple = pygame.color.THECOLORS['red']):
        self.x, self.y = coord
        self.size = size
        self.color = color
        try:
            self.img = pygame.image.load('images/apple.png')
            self.img = pygame.transform.scale(self.img, self.size)
        except FileNotFoundError:
            self.img = None

    def draw(self, surface: pygame.Surface):
        if self.img:
            surface.blit(self.img, [(self.x, self.y), self.size])
        else:
            pygame.draw.rect(surface, self.color, [(self.x, self.y), self.size])
