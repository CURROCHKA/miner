from enum import Enum


PLAYERS = 8

WINDOW_SIZE = (1280, 1024)
GRID_SIZE = (800, 600)


class Color(Enum):
    WHITE = {0: (255, 255, 255)}
    RED = {1: (255, 0, 0)}
    GREEN = {2: (0, 255, 0)}
    BLUE = {3: (0, 0, 255)}
    YELLOW = {4: (255, 255, 0)}
    PINK = {5: (255, 0, 255)}
    BROWN = {6: (150, 75, 0)}
    BLACK = {7: (0, 0, 0)}
