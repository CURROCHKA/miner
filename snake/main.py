import sys
from random import choice, randrange
from typing import Literal

import pygame_widgets
from pygame_widgets.button import Button

from config import *
from snake import Snake
from fruit import Fruit


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_size = self.screen.get_size()
        self.font_size = int(self.screen_size[0] * FONT_SIZE)
        self.font_style = pygame.font.SysFont('consolas', self.font_size)
        self.cell_size = int(self.screen_size[0] * CELL_X), int(self.screen_size[1] * CELL_Y)
        self.clock = pygame.time.Clock()
        self.frame = 5
        self.score = 0
        self.game_over = False
        self.snake = Snake(self._get_snake_coord(), self.cell_size)
        self.fruit = Fruit(self._get_fruit_coord(), self.cell_size)
        self.play_button = Button(
            onRelease=self.unpause,
            **self._set_buttons_args(pos='top', text='Продолжить'),
        )
        self.quit_button = Button(
            onRelease=self.exit_game,
            **self._set_buttons_args(pos='bottom', text='Выход'),
        )
        try:
            self.background = pygame.image.load('images/background.png').convert_alpha()
            self.background = pygame.transform.scale(surface=self.background, size=self.screen_size)
        except FileNotFoundError:
            self.background = None
        pygame.display.set_caption('Snake')

    def run(self) -> None:
        while True:
            events = pygame.event.get()
            self.check_events(events)
            self.snake.update(self.screen_size)
            self.update_screen(events)
            if self.snake.check_intersection():
                self.game_over = True
                self.snake.moving = 0
                self.play_button.setOnRelease(self.game_reset)
                self.play_button.setText('Новая игра')

    def unpause(self) -> None:
        self.snake.moving = 1

    def game_reset(self) -> None:
        self.score = 0
        self.frame = 5
        self.game_over = False
        self.snake = Snake(self._get_snake_coord(), self.cell_size)
        self.fruit = Fruit(self._get_fruit_coord(), self.cell_size)
        self.play_button.setOnRelease(self.unpause)
        self.play_button.setText('Продолжить')

    @staticmethod
    def exit_game() -> None:
        pygame.quit()
        sys.exit()

    def _set_buttons_args(self, pos: Literal['top', 'bottom'], text: str = '') -> dict[str, float]:
        center_x = self.screen_size[0] // 2
        center_y = self.screen_size[1] // 2
        margin_button = int(self.screen_size[1] * BUTTON_DISTANCE)
        size = self.font_style.size(text)
        width = int(size[0] * BUTTON_WIDTH)
        height = int(size[1] * BUTTON_HEIGHT)
        x = center_x - size[0] // 2
        y = center_y - size[1] // 2
        radius = int(size[0] * BUTTON_RADIUS)
        border_thickness = int(self.screen_size[0] * BUTTON_THICKNESS)
        if pos == 'top':
            y -= margin_button
        elif pos == 'bottom':
            y += margin_button

        return {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'text': text,
            'radius': radius,
            'win': self.screen,
            'font': self.font_style,
            'textColour': Colors.WHITE.value,
            'colour': Colors.RED.value,
            'borderThickness': border_thickness,
            'borderColour': Colors.WHITE.value,
            'pressedBorderColour': Colors.GREEN.value,
            'hoverBorderColour': Colors.RED.value,
        }

    def _get_snake_coord(self) -> tuple[int, int]:
        center_x = self.screen_size[0] // 2
        center_y = self.screen_size[1] // 2
        x = center_x - center_x % self.cell_size[0]
        y = center_y - center_y % self.cell_size[1]
        return x, y

    def _get_fruit_coord(self) -> tuple[int, int]:
        space_x = int(self.screen_size[0] - self.screen_size[0] % self.cell_size[0] - self.cell_size[0])
        space_y = int(self.screen_size[1] - self.screen_size[1] % self.cell_size[1] - self.cell_size[1])

        while True:
            x = randrange(0, space_x, self.cell_size[0])
            y = randrange(0, space_y, self.cell_size[1])
            if (x, y) not in self.snake.elements:
                return x, y

    def check_events(self, events: pygame.event) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
            if event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
        self.check_fruit_consume()

    def check_fruit_consume(self) -> None:
        head_coord = self.snake.elements[0]
        if head_coord == (self.fruit.x, self.fruit.y):
            self.snake.add_elem()
            self.score += 1
            self.fruit.x, self.fruit.y = self._get_fruit_coord()
            if self.frame <= 15 and self.score % 3 == 0:
                self.frame += 1  # Увеличение скорости игры
            self.snake.color = choice([color.value for color in Colors])

    def check_keydown_events(self, event: pygame.event.Event) -> None:
        press_key = event.key
        directions = {
            pygame.K_w: (0, -1),  # Вверх
            pygame.K_UP: (0, -1),  # Вверх
            pygame.K_a: (-1, 0),  # Влево
            pygame.K_LEFT: (-1, 0),  # Влево
            pygame.K_s: (0, 1),  # Вниз
            pygame.K_DOWN: (0, 1),  # Вниз
            pygame.K_d: (1, 0),  # Вправо
            pygame.K_RIGHT: (1, 0)  # Вправо
        }

        if press_key == pygame.K_ESCAPE and not self.game_over:
            self.snake.moving = 0 if self.snake.moving == 1 else 1
        if press_key in directions and self.snake.moving != 0:
            dx, dy = directions[press_key]
            self.snake.direction_buffer.append((dx, dy))

    def print_message(
            self,
            msg: str,
            color: tuple[int, int, int, int] | tuple[int, int, int],
            pos: tuple
    ) -> None:
        print_msg = self.font_style.render(msg, True, color)
        size = self.font_style.size(msg)
        rect = [pos[0], pos[1], size[0], size[1]]
        self.screen.blit(source=print_msg, dest=rect)

    def update_screen(self, events: pygame.event) -> None:
        if self.background:
            self.screen.blit(source=self.background, dest=self.background.get_rect())
        else:
            self.screen.fill(color=Colors.GRAY.value)
        self.print_message(
            msg=f'Score {self.score}',
            color=Colors.YELLOW.value,
            pos=(self.screen_size[0] // 2 - self.font_style.size('Score')[0] // 2, 0))
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)
        if self.snake.moving != 0:
            self.clock.tick(self.frame)
        else:
            pygame_widgets.update(events)
        pygame.display.update()


if __name__ == '__main__':
    snake_game = Game()
    snake_game.run()
