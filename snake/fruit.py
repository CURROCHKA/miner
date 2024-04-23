import pygame
from config import Colors


class Fruit:
    def __init__(
            self,
            coord: tuple[int, int],
            size: tuple[int, int],
            color: tuple[int, int, int, int] = Colors.RED.value
    ):
        self.x, self.y = coord
        self.size = size
        self.color = color
        try:
            self.img = pygame.image.load('images/apple.png').convert_alpha()
            self.img = pygame.transform.scale(surface=self.img, size=self.size)
        except FileNotFoundError:
            self.img = None

    def draw(self, surface: pygame.Surface) -> None:
        if self.img:
            surface.blit(source=self.img, dest=[(self.x, self.y), self.size])
        else:
            pygame.draw.rect(surface=surface, color=self.color, rect=[(self.x, self.y), self.size])
