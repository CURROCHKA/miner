import pygame
from collections import deque


class Snake:
    def __init__(self, coord: tuple[int, int], size: tuple[int, int], color: tuple = pygame.color.THECOLORS['green']):
        self.x, self.y = coord
        self.size = size
        self.color = color
        self.snake_list = [(self.x, self.y)]
        self.moving_x, self.moving_y = 0, 0
        self.speed = 1
        self.len = 1
        self.direction_buffer = deque(maxlen=2)  # Буфер направлений движения змейки
        # (можно "запомнить" максимум 2 хода змейки)

    def update(self, screen_size: tuple[int, int]):
        if self.direction_buffer:
            if self.len == 1:  # Если у змейки длина 1 - она может двигаться в любых направлениях
                self.moving_x, self.moving_y = self.direction_buffer.popleft()
            elif (self.direction_buffer[0][0], self.direction_buffer[0][1]) != (-self.moving_x, -self.moving_y):
                # Проверка на совпадение первого направления в буфере с противоположным направлением змейки для того,
                # чтобы не было поворота на 180 градусов (чтобы змейка не пошла в себя)
                self.moving_x, self.moving_y = self.direction_buffer.popleft()
            else:
                self.direction_buffer.popleft()
        self.x += self.size[0] * self.moving_x * self.speed
        self.y += self.size[1] * self.moving_y * self.speed
        self._check_edges(screen_size)

        # ОБНОВЛЕНИЕ snake_list путем добавления ячейки змеи в список и удаление, если фактическая длина змеи меньше
        if self.speed == 1:
            self.snake_list.append((self.x, self.y))
        if len(self.snake_list) > self.len:
            del self.snake_list[0]

    def _check_edges(self, screen_size: tuple[int, int]):
        width = screen_size[0]
        height = screen_size[1]
        leftover_x = width % self.size[0]
        leftover_y = height % self.size[1]
        if self.x < 0:
            self.x = width - leftover_x - self.size[0]
        elif self.x >= width - leftover_x:
            self.x = 0
        if self.y < 0:
            self.y = height - leftover_y - self.size[1]
        elif self.y >= height - leftover_y:
            self.y = 0

    def check_collisions(self):
        return self.len >= 4 and self.snake_list[0] in self.snake_list[1:]

    def draw(self, surface: pygame.Surface):
        for cell in self.snake_list:
            rect = [cell[0], cell[1], self.size[0], self.size[1]]
            pygame.draw.rect(surface, self.color, rect)
