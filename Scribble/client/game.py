import sys
from math import hypot

import pygame
import pygame_widgets
from pygame_widgets.button import Button

from board import Board
from top_bar import TopBar
from main_menu import MainMenu
from chat import Chat
from bottom_bar import BottomBar
from leaderboard import LeaderBoard
from player import Player

from config import (
    FRAME,
    COLORS,
    WINDOW_SIZE,
    MARGIN,
    PLAYERS,
    BORDER_THICKNESS,
    SKIP_FONT_SIZE,
    BOARD_WIDTH,
    LEADERBOARD_WIDTH,
    TOP_BAR_WIDTH,
    BOTTOM_BAR_WIDTH,
)

from typing import Any, Literal

# for test
WINDOW_SIZE = (1360, 768)
# WINDOW_SIZE = (1920, 1080)
# WINDOW_SIZE = (1300, 1000)
# WINDOW_SIZE = (1366, 768)
# WINDOW_SIZE = (1280, 1024)


class Game:
    def __init__(self):
        self.width, self.height = WINDOW_SIZE
        # self.win = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)  # original
        self.win = pygame.display.set_mode((self.width, self.height))  # for test
        self.width, self.height = self.win.get_size()
        pygame.display.set_caption('Scribble')
        self.BG_color = COLORS[0]
        self.draw_color = COLORS[7]
        self.margin = self.width * MARGIN / 100

        self.top_bar = TopBar(self.win, **self.__set_top_bar())
        self.leaderboard = LeaderBoard(self.win, **self.__set_leaderboard())
        self.board = Board(self.win, **self.__set_board())
        self.chat = Chat(self.win, **self.__set_chat())
        # self.top_bar.change_round(1)

        self.players = [Player('Ivan'), Player('Polina'), Player('Иван Назаров'), Player('QQQQQQQQQQQQQQ'),
                        Player('Ivan'), Player('Polina'), Player('Иван Назаров'), Player('I')]

        self.skip_button = Button(self.win, **self.__set_skip_button())
        self.bottom_bar = BottomBar(self.win, **self.__set_bottom_bar(), game=self)

        for player in self.players:
            self.leaderboard.add_player(player)

        self.last_pos = None

    def set_draw_color(self, draw_color: tuple[int, int, int]):
        self.draw_color = draw_color

    def __set_chat(self) -> dict[str, Any]:
        x = self.board.width + self.leaderboard.width + self.margin * 3
        y = self.board.y
        width = self.width - x - self.margin
        height = self.height - self.top_bar.height - self.margin * 2
        args = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'margin': self.margin,
        }
        return args

    def __set_bottom_bar(self) -> dict[str, Any]:
        args = {
            'x': int(self.board.x),
            'y': int(self.board.y + self.board.height + self.margin),
            'width': int(self.board.width / BOTTOM_BAR_WIDTH),
            'height': int(self.leaderboard.height * 2),
            'margin': self.margin
        }
        return args

    def __set_skip_button(self) -> dict[str, Any]:
        x = self.leaderboard.width / 4 + self.margin
        y = self.leaderboard.height * len(self.players) + self.top_bar.height + self.margin * 3
        width = self.leaderboard.width / 2
        height = self.leaderboard.height
        text = 'Skip'
        border_thickness = int(self.margin / BORDER_THICKNESS)
        font_size = int(height / len(text) * SKIP_FONT_SIZE)
        font = pygame.font.SysFont('consolas', font_size, bold=True)
        on_click = self.skip
        args = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'colour': COLORS[4],
            'text': text,
            'borderThickness': border_thickness,
            'fontSize': font_size,
            'font': font,
            'onClick': on_click
        }
        return args

    def __set_board(self) -> dict[str, Any]:
        x = self.leaderboard.width + self.margin * 2
        y = self.top_bar.height + self.margin * 2
        width = int(self.width / BOARD_WIDTH)
        height = int(self.leaderboard.height * PLAYERS)
        args = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'margin': self.margin
        }
        return args

    def __set_leaderboard(self) -> dict[str, Any]:
        args = {
            'x': self.margin,
            'y': self.top_bar.height + self.margin * 2,
            'width': self.top_bar.width / LEADERBOARD_WIDTH + self.margin,
            'height': self.margin * (PLAYERS - 2),
            'margin': self.margin
        }
        return args

    def __set_top_bar(self) -> dict[str, Any]:
        args = {
            'x': self.margin,
            'y': self.margin,
            'width': self.width - self.margin * 2,
            'height': self.height / TOP_BAR_WIDTH,
            'margin': self.margin
        }
        return args

    @staticmethod
    def interpolate_points(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        distance = int(hypot(x2 - x1, y2 - y1))
        points = [(x1 + i * (x2 - x1) // distance, y1 + i * (y2 - y1) // distance) for i in range(distance)]
        return points

    def update_skip_button_pos(self, direction: Literal[1, -1]):
        self.skip_button.moveY(self.leaderboard.height * direction)

    def skip(self):
        print('Clicked skip button')

    def check_cliks(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.last_pos:
            for point in self.interpolate_points(self.last_pos, mouse_pos):
                clicked_board = self.board.click(*point)
                if clicked_board:
                    self.board.update(*clicked_board, self.draw_color)

        clicked_board = self.board.click(*mouse_pos)
        if clicked_board:
            self.board.update(*clicked_board, self.draw_color)

        self.last_pos = mouse_pos

    def draw(self, events):
        self.win.fill(self.BG_color)
        self.leaderboard.draw()
        self.top_bar.draw()
        self.board.draw()
        self.chat.draw()

        pygame_widgets.update(events)
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        pygame.event.set_allowed([pygame.MOUSEMOTION, pygame.QUIT])
        while True:
            events = pygame.event.get()
            clock.tick(FRAME)
            self.draw(events)
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:
                    self.check_cliks()
                else:
                    self.last_pos = None


if __name__ == '__main__':
    pygame.font.init()
    g = Game()
    g.run()
