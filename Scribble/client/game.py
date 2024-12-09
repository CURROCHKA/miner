from math import hypot
from typing import Any, Literal

import pygame
import pygame_widgets
from pygame_widgets.button import Button

from board import Board
from top_bar import TopBar
from chat import Chat
from bottom_bar import BottomBar
from leaderboard import LeaderBoard
from player import Player

from config import (
    Window,
    FRAME,
    COLORS,
    WINDOW_SIZE,
    MARGIN,
    BORDER_THICKNESS,
    SKIP_FONT_SIZE,
    BOARD_WIDTH,
    BOTTOM_BAR_WIDTH,
    MAX_PLAYERS,
)


# for test
WINDOW_SIZE = (1360, 768)
# WINDOW_SIZE = (1920, 1080)
# WINDOW_SIZE = (1300, 1000)
# WINDOW_SIZE = (1366, 768)
# WINDOW_SIZE = (1280, 1024)


class Game(Window):
    def __init__(self, connection=None):
        pygame.init()
        super().__init__(WINDOW_SIZE[0], WINDOW_SIZE[1], caption='Scribble', frame=FRAME)
        self.connection = connection

        self.draw_color = COLORS[7]
        self.margin = self.width * MARGIN / 100

        self.top_bar = TopBar(self.win, **self.__set_top_bar())
        self.top_bar.change_round(1)
        self.leaderboard = LeaderBoard(self.win, **self.__set_leaderboard())
        self.board = Board(self.win, **self.__set_board(), game=self)
        self.chat = Chat(self.win, **self.__set_chat(), game=self)

        self.players = []
        for player in self.players:
            self.leaderboard.add_player(player)

        self.skip_button = Button(self.win, **self.__set_skip_button())
        self.bottom_bar = BottomBar(self.win, **self.__set_bottom_bar(), game=self)

        self.last_pos = None
        self.drawing = False

    def add_player(self, player):
        self.players.append(player)
        self.leaderboard.add_player(player)
        self.update_skip_button_pos(direction=1)

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
        height = int(self.leaderboard.height * MAX_PLAYERS)
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
            'width': self.top_bar.width / 6 + self.margin,
            'height': self.top_bar.height,
            'margin': self.margin
        }
        return args

    def __set_top_bar(self) -> dict[str, Any]:
        args = {
            'x': self.margin,
            'y': self.margin,
            'width': self.width - self.margin * 2,
            'height': self.height / 12,
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
        self.connection.send({1: []})

    def decode_color(self):
        for key in COLORS:
            if COLORS[key] == self.draw_color:
                return key

    def check_cliks(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.last_pos:
            for point in self.interpolate_points(self.last_pos, mouse_pos):
                clicked_board = self.board.click(*point)
                if clicked_board:
                    self.board.update(*clicked_board, self.draw_color)
                    if self.connection:
                        self.connection.send({7: [*clicked_board, self.decode_color()]})

        clicked_board = self.board.click(*mouse_pos)
        if clicked_board:
            self.board.update(*clicked_board, self.draw_color)
            if self.connection:
                self.connection.send({7: [*clicked_board, self.decode_color()]})

        self.last_pos = mouse_pos

    def set_board(self):
        board = self.connection.send({3: []})
        self.board.compressed_grid = board
        self.board.translate_board()

    def set_time(self):
        response = self.connection.send({8: []})
        self.top_bar.time = response

    def set_chat_content(self):
        response = self.connection.send({2: []})
        self.chat.update_chat(response)

    def set_word(self):
        word = self.connection.send({6: []})
        self.top_bar.change_word(word)

    def set_round(self):
        rnd = self.connection.send({5: []})
        self.top_bar.change_round(rnd)

    def set_drawing(self):
        drawing = self.connection.send({10: []})
        self.drawing = drawing

    def set_top_bar_info(self):
        self.top_bar.max_round = len(self.players)
        self.top_bar.drawing = self.drawing

    def draw(self, events):
        self.clock.tick(self.frame)
        self.win.fill(self.BG_color)
        self.leaderboard.draw()
        self.top_bar.draw()
        self.board.draw()
        self.chat.draw()

        self.bottom_bar.color_buttons.show()
        self.bottom_bar.color_buttons.enable()

        self.bottom_bar.spec_buttons.show()
        self.bottom_bar.spec_buttons.enable()

        self.chat.text_box.hide()
        self.chat.text_box.disable()

        self.skip_button.show()
        self.skip_button.enable()

        if not self.drawing:
            self.bottom_bar.color_buttons.hide()
            self.bottom_bar.color_buttons.disable()

            self.bottom_bar.spec_buttons.hide()
            self.bottom_bar.spec_buttons.disable()

            self.chat.text_box.show()
            self.chat.text_box.enable()

            self.skip_button.hide()
            self.skip_button.disable()

        pygame_widgets.update(events)
        pygame.display.flip()

    def check_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                # self.leaderboard.remove_player()
                pygame.quit()
                quit()
            if pygame.mouse.get_pressed()[0]:
                self.check_cliks()
            else:
                self.last_pos = None

    def run(self):
        pygame.event.set_allowed([pygame.MOUSEMOTION, pygame.QUIT])
        while True:
            events = pygame.event.get()
            try:
                # get board
                self.set_board()

                # get time
                self.set_time()

                # get chat
                self.set_chat_content()

                # get round information
                self.set_word()
                self.set_round()
                self.set_drawing()
                self.set_top_bar_info()

                # get players update
                # response = self.connection.send({-1: []})
                # self.players = []
                # self.leaderboard.players = []
                # self.skip_button = Button(self.win, **self.__set_skip_button())
                # for player_name in response:
                #     player = Player(player_name)
                #     self.players.append(player)
                #     self.leaderboard.add_player(player)
                #     self.update_skip_button_pos(direction=1)

            except Exception as e:
                print(e)

            self.check_events(events)
            self.draw(events)
