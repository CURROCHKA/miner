import pygame


class Cross:
    def __init__(self, window: pygame.Surface, x: int, y: int, cell_size: tuple[int, int], width: int, color='black'):
        self.window = window
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.width = width
        self.color = color

    def draw(self):
        cell_x, cell_y = self.cell_size
        offset_x = cell_x / 2
        offset_y = cell_y / 2

        for i in range(-1, 2, 2):
            start_pos = (self.x - offset_x * i, self.y - offset_y)
            end_pos = (self.x + offset_x * i, self.y + offset_y)

            pygame.draw.line(surface=self.window,
                             color=self.color,
                             start_pos=start_pos,
                             end_pos=end_pos,
                             width=self.width)
