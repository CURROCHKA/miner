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
        self.is_move_done = False
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
            'fontSizes': [self.cell_x] * 9,
        }

    def update(self, player: str) -> None:
        self.is_move_done = False
        for button in self.buttons.getButtons():
            if button.clicked and button.string == '':
                button.setText(player)
                self.is_move_done = True

    def check_columns(self):
        buttons = self.buttons.getButtons()
        for i in range(0, len(buttons), 3):
            seq = [button.string for button in buttons[i: i + 3]]
            if self.check_sequence(seq):
                return True
        return False

    def check_rows(self):
        buttons = self.buttons.getButtons()
        for i in range(len(buttons) - 6):
            seq = [buttons[i].string, buttons[i + 3].string, buttons[i + 6].string]
            if self.check_sequence(seq):
                return True
        return False

    def check_diagonals(self) -> bool:
        buttons = self.buttons.getButtons()
        seq = [buttons[0].string, buttons[4].string, buttons[8].string]
        if self.check_sequence(seq):
            return True

        seq = [buttons[6].string, buttons[4].string, buttons[2].string]
        if self.check_sequence(seq):
            return True
        return False

    @staticmethod
    def check_sequence(seq) -> bool:
        set_seq = set(seq)
        return set_seq != {''} and len(set_seq) == 1

    def check_field(self) -> bool:
        return self.check_columns() or self.check_rows() or self.check_diagonals()
