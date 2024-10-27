class Board:
    def __init__(self, x: float, y: float, grid_size: tuple[int, int], cell_size: tuple[int, int]):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = self.create_empty_board()
        self.width = self.grid_size[0] * self.cell_size[0]
        self.height = self.grid_size[1] * self.cell_size[1]

    def update(self, x: int, y: int, color: tuple[int, int, int]):
        self.grid[y][x] = color

    def create_empty_board(self) -> list[list[tuple[int, int, int]]]:
        return [[(255, 255, 255) for _ in range(self.grid_size[1]) for _ in range(self.grid_size[0])]]

    def clear(self):
        self.grid = self.create_empty_board()

    def fill(self, x, y):
        pass

    def get_board(self):
        return self.grid
