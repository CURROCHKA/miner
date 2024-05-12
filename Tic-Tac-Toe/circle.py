import pygame


class Circle:
    def __init__(self, window: pygame.Surface, x: int, y: int, radius: int, width: int, color='black'):
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        self.color = color

    def draw(self):
        pygame.draw.circle(surface=self.window,
                           color=self.color,
                           center=(self.x, self.y),
                           radius=self.radius,
                           width=self.width)

