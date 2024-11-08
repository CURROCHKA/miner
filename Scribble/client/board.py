from config import (
    COLORS,
    BORDER_THICKNESS,
    ROWS,
    COLS,
)

import pygame


class Board:
    def __init__(self, win: pygame.Surface, x: float, y: float, width: int, height: int, margin: float):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = margin
        self.width = width
        self.height = height

        # Делаю квадратные пиксели
        self.pixel_size = self.__get_pixel_size()
        # Перерасчет ширины и высоты, относительно pixel_size
        self.width = self.pixel_size * COLS
        self.height = self.pixel_size * ROWS

        self.border_thickness = int(self.margin / BORDER_THICKNESS)
        self.grid = self.create_empty_board()
        self.compressed_grid = []

    def __get_pixel_size(self) -> int:
        pixel_size_x = self.width // COLS
        pixel_size_y = self.height // ROWS
        if self.width - 10 <= pixel_size_x * COLS <= self.width + 10:
            # Нельзя превышать заданную ширину менее или более, чем на 10 пикселей
            pixel_size = pixel_size_x
        else:
            # Среднее арифметическое pixel_size_x и pixel_size_y
            pixel_size = (pixel_size_x + pixel_size_y) / 2
        return int(pixel_size)

    def draw(self):
        for y, _ in enumerate(self.grid):
            for x, color in enumerate(self.grid[y]):
                pygame.draw.rect(self.win, color, (self.x + x * self.pixel_size,
                                                   self.y + y * self.pixel_size,
                                                   self.pixel_size, self.pixel_size), 0)

        pygame.draw.rect(self.win, COLORS[7], (self.x - self.border_thickness / 2,
                                               self.y - self.border_thickness / 2,
                                               self.width + self.border_thickness,
                                               self.height + self.border_thickness), self.border_thickness)

    @staticmethod
    def check_coord(row: int, col: int):
        return 0 <= row < ROWS and 0 <= col < COLS

    def click(self, x: int, y: int) -> tuple[int, int]:
        row = int((x - self.x) / self.pixel_size)
        col = int((y - self.y) / self.pixel_size)

        if self.check_coord(col, row):
            return row, col

    def update(self, x: int, y: int, color: tuple[int, int, int] | int, thickness: int = 0):
        neighbours = {(x, y)}
        for _ in range(thickness // 2):
            for n in list(neighbours):
                neighs = self.get_neighbour(*n)
                for neighbour in neighs:
                    neighbours.add(neighbour)

        for x, y in list(neighbours):
            if self.check_coord(y, x):
                self.grid[y][x] = color

    @staticmethod
    def get_neighbour(x: int, y: int) -> list[tuple[int, int]]:
        return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y),
                (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

    @staticmethod
    def create_empty_board() -> list[list[int]]:
        return [[COLORS[0] for _ in range(COLS)] for _ in range(ROWS)]

    def translate_board(self):
        for y, _ in enumerate(self.compressed_grid):
            for x, color in enumerate(self.compressed_grid[y]):
                self.grid[y][x] = COLORS[color]

    def clear(self):
        self.grid = self.create_empty_board()

    def get_board(self):
        return self.grid
