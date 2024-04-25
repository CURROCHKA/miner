from collections import deque
from config import Colors

import pygame


class Snake:
    def __init__(
            self,
            head_coord: tuple[int, int],
            size: tuple[int, int],
            color: tuple[int, ...] = Colors.GREEN.value
    ):
        self.cell_size = size
        self.color = color
        self.elements = [head_coord]
        self.moving_x, self.moving_y = 0, 0
        self.moving = 1
        self.direction_buffer = deque(maxlen=2)  # Буфер направлений движения змейки
        # (можно "запомнить" максимум 2 хода змейки)

    def update(self, screen_size: tuple[int, int]) -> None:
        if self.moving:
            self.direction_update()
            elements_copy = self.elements.copy()
            head_x, head_y = self.elements[0]
            head_x += self.cell_size[0] * self.moving_x
            head_y += self.cell_size[1] * self.moving_y
            self.elements[0] = (head_x, head_y)
            for i in range(1, len(self.elements)):
                self.elements[i] = elements_copy[i - 1]  # Каждый элемент змейки двигается на место впередистоящего
                # элемента
            self._check_edges(screen_size)

    def direction_update(self):
        if self.direction_buffer:
            if len(self.elements) == 1:  # Если у змейки длина 1 - она может двигаться в любых направлениях
                self.moving_x, self.moving_y = self.direction_buffer.popleft()
            elif (self.direction_buffer[0][0], self.direction_buffer[0][1]) != (-self.moving_x, -self.moving_y):
                # Проверка на совпадение первого направления в буфере с противоположным направлением змейки для
                # того, чтобы не было поворота на 180 градусов (чтобы змейка не пошла в себя)
                self.moving_x, self.moving_y = self.direction_buffer.popleft()
            else:
                self.direction_buffer.popleft()

    def add_element(self):
        head_x, head_y = self.elements[0]
        x, y = (head_x - self.cell_size[0] * self.moving_x, head_y - self.cell_size[1] * self.moving_y)
        self.elements.append((x, y))

    def _check_edges(self, screen_size: tuple[int, int]) -> None:
        width = screen_size[0]
        height = screen_size[1]
        leftover_x = width % self.cell_size[0]
        leftover_y = height % self.cell_size[1]
        head_x, head_y = self.elements[0]
        if head_x < 0:
            head_x = width - leftover_x - self.cell_size[0]
        elif head_x >= width - leftover_x:
            head_x = 0
        if head_y < 0:
            head_y = height - leftover_y - self.cell_size[1]
        elif head_y >= height - leftover_y:
            head_y = 0
        self.elements[0] = (head_x, head_y)

    def check_intersection(self) -> bool:
        return len(self.elements) >= 4 and self.elements[0] in self.elements[1::]  # Змейка длиной <= 4 не может себя
        # съесть

    def draw(self, surface: pygame.Surface) -> None:
        for element in self.elements:
            x, y = element
            rect = [x, y, self.cell_size[0], self.cell_size[1]]
            pygame.draw.rect(surface=surface, color=self.color, rect=rect)
