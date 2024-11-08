from typing import Any

import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox

from network import Network
from game import Game
from player import Player
from config import (
    Window,
    WINDOW_SIZE,
    COLORS,
    FRAME,
    FONT_NAME,
)

# for test
WINDOW_SIZE = (1360, 768)
# WINDOW_SIZE = (1920, 1080)
# WINDOW_SIZE = (1300, 1000)
# WINDOW_SIZE = (1366, 768)
# WINDOW_SIZE = (1280, 1024)


class MainMenu(Window):
    def __init__(self):
        super().__init__(WINDOW_SIZE[0], WINDOW_SIZE[1], caption='Scribble', frame=FRAME)
        self.network = None

        self.text_box = TextBox(self.win,
                                **self.__set_text_box(),
                                placeholderText='Enter your nickname',
                                onSubmit=self.text_box_submit)

        self.title_font_size = int(self.width / 15)
        self.title_font = pygame.font.SysFont(FONT_NAME, self.title_font_size)

        self.enter_font_size = int(self.width / 30)
        self.enter_font = pygame.font.SysFont(FONT_NAME, self.enter_font_size)

        self.waiting = False

    def __set_text_box(self) -> dict[str, Any]:
        width = self.width / 3
        height = self.height / 10
        x = self.width / 2 - width / 2
        y = self.height / 2 - height / 2
        font_size = int(width / 15)
        font = pygame.font.SysFont(FONT_NAME, font_size)
        args = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'fontSize': font_size,
            'font': font,
        }
        return args

    def text_box_submit(self):
        name = self.text_box.getText()
        if len(name) >= 1:
            self.waiting = True
            self.text_box.hide()
            self.text_box.disable()
            self.network = Network(name)

    def draw(self, events: list[pygame.event.Event]):
        self.clock.tick(self.frame)
        self.win.fill(COLORS[0])

        title = self.title_font.render('Scribble', 1, COLORS[7])
        self.win.blit(title, (self.width / 2 - title.get_width() / 2, 0))

        if self.waiting:
            enter = self.enter_font.render('In queue', 1, COLORS[7])
        else:
            enter = self.enter_font.render('Press enter to join a game...', 1, COLORS[7])
        self.win.blit(enter, (self.width / 2 - enter.get_width() / 2, title.get_height()))

        pygame_widgets.update(events)
        pygame.display.flip()

    def check_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def run(self):
        while True:
            events = pygame.event.get()
            if self.waiting:
                response = self.network.send({-1: []})
                if response:
                    game = Game(self.network)
                    for player_name in response[0].keys():
                        player = Player(player_name)
                        game.add_player(player)
                    game.run()
                    break
            self.check_events(events)
            self.draw(events)


if __name__ == '__main__':
    pygame.init()
    main = MainMenu()
    main.run()
