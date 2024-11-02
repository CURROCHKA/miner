from config import (
    Color,
    GRID_SIZE,
)


class Board:
    def __init__(self):
        self.grid = self.create_empty_board()

    def update(self, x: int, y: int, color: tuple[int, int, int] | int):
        self.grid[y][x] = color

    @staticmethod
    def create_empty_board() -> list[list[int]]:
        color = list(Color.WHITE.value.keys())[0]
        return [[color for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]

    def clear(self):
        self.grid = self.create_empty_board()

    def fill(self, x, y):
        pass

    def get_board(self):
        return self.grid
