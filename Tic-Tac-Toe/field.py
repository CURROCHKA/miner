import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray


class Field:
    def __init__(self, window: pygame.Surface, cell_size: tuple[int, int], line_width: int):
        pygame.init()

        self.window = window
        self.window_size = self.window.get_size()
        self.window_width, self.window_height = self.window_size
        self.cell_x, self.cell_y = cell_size
        self.line_width = line_width
        self.field_size = self.get_available_space()
        self.buttons = ButtonArray(
            **self.get_buttons_params()
        )

    def draw(self) -> None:
        pygame_widgets.update(pygame.event.get())
        available_space_x, available_space_y = self.field_size

        for i in range(1, 3):
            horizontal_x = available_space_x / 2
            horizontal_y = available_space_y / 2 + self.cell_y * i

            vertical_x = available_space_x / 2 + self.cell_x * i
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

    def get_available_space(self) -> tuple[float, float]:
        available_space_x = self.window_width - (self.cell_x * 3)
        available_space_y = self.window_height - (self.cell_y * 3)
        return available_space_x, available_space_y

    def get_buttons_params(self) -> dict:
        return {
            'win': self.window,
            'x': self.field_size[0] / 2,
            'y': self.field_size[1] / 2,
            'width': self.cell_x * 3,
            'height': self.cell_y * 3,
            'shape': [3, 3],
            'border': 0,
            'inactiveColours': ['gray'] * 9,
        }
