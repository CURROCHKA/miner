import pygame


LINE_WIDTH = 0.00234


class Field:
    def __init__(self, window: pygame.Surface, cell_size: tuple[int, int]):
        self.window = window
        self.window_size = self.window.get_size()
        self.window_width, self.window_height = self.window_size[0], self.window_size[1]
        self.cell_size = cell_size
        self.line_width = int(self.window_width * LINE_WIDTH)

    def draw(self) -> None:
        cell_x, cell_y = self.cell_size[0], self.cell_size[1]
        available_space_x = self.window_width - (cell_x * 3)
        available_space_y = self.window_height - (cell_y * 3)

        for i in range(1, 3):
            horizontal_x = available_space_x / 2
            horizontal_y = available_space_y / 2 + cell_y * i

            vertical_x = available_space_x / 2 + cell_x * i
            vertical_y = available_space_y / 2
            pygame.draw.lines(surface=self.window,
                              color='black',
                              closed=False,
                              points=[(horizontal_x, horizontal_y),
                                      (self.window_width - horizontal_x, horizontal_y)], width=self.line_width)
            pygame.draw.lines(surface=self.window,
                              color='black',
                              closed=False,
                              points=[(vertical_x, vertical_y),
                                      (vertical_x, self.window_height - vertical_y)], width=self.line_width)
