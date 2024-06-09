from enum import Enum

import pygame


FONT_SIZE = 0.045
CELL_X = 0.013
CELL_Y = 0.0231
BUTTON_WIDTH = 1.15
BUTTON_HEIGHT = 1.3
BUTTON_RADIUS = 0.5
BUTTON_THICKNESS = 0.00275
BUTTON_DISTANCE = 0.075


class Colors(Enum):
    RED = pygame.color.THECOLORS['red']
    GREEN = pygame.color.THECOLORS['green']
    WHITE = pygame.color.THECOLORS['white']
    GRAY = pygame.color.THECOLORS['gray']
    YELLOW = pygame.color.THECOLORS['yellow']


class Directions(Enum):
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    RIGHT = (1, 0)
