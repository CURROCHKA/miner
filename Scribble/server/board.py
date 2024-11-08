from config import (
    COLS,
    ROWS,
)


class Board:
    def __init__(self):
        self.grid = self.create_empty_board()

    @staticmethod
    def check_coord(row: int, col: int):
        return 0 <= row < ROWS and 0 <= col < COLS

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
        return [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def clear(self):
        self.grid = self.create_empty_board()

    def get_board(self):
        return self.grid
