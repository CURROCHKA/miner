from enum import Enum


class Color(Enum):
    WHITE = {0: (255, 255, 255)}
    RED = {1: (255, 0, 0)}
    GREEN = {2: (0, 255, 0)}
    BLUE = {3: (0, 0, 255)}
    YELLOW = {4: (255, 255, 0)}
    PINK = {5: (255, 0, 255)}
    BROWN = {6: (150, 75, 0)}
    BLACK = {7: (0, 0, 0)}
    GRAY = {8: (200, 200, 200)}


FRAME = 120
WINDOW_SIZE = (0, 0)
COLS, ROWS = (160, 90)
FONT_NAME = 'consolas'

# as a percentage
MARGIN = 0.78125
PIXEL_SIZE_X = 0.121293
PIXEL_SIZE_Y = 0.18480

BORDER_THICKNESS = 2.5
# BOARD_WIDTH = 1.8
BOARD_WIDTH = 1.6
LEADERBOARD_WIDTH = 6
TOP_BAR_WIDTH = 12
BOTTOM_BAR_WIDTH = 2.5
SKIP_FONT_SIZE = 1.5
CHAT_FONT_SIZE = 15

PLAYERS = 8
MAX_ROUND = 8
COLORS = {list(color.value.keys())[0]: list(color.value.values())[0] for color in Color}
