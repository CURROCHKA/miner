import pygame
from pygame_widgets.button import ButtonArray

from config import (
    COLORS
)


class BottomBar:
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, margin: float, game):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = margin
        self.game = game
        self.color_buttons = ButtonArray(
            self.win,
            self.x,
            self.y,
            self.width,
            self.height,
            (4, 2),
            border=0,
            colour=COLORS[0],
            inactiveColours=list(COLORS.values())[1::],
            separationThickness=0,
            onClicks=[self.color_click] * 8
        )

        try:
            self.erase_img = pygame.image.load('images/eraser.png').convert_alpha()
            self.erase_img.set_colorkey(COLORS[0])
            self.erase_img = pygame.transform.scale(self.erase_img, (self.height, self.height))
            self.erase_text = ''
            self.erase_color = COLORS[0]
        except Exception as e:
            print(e)
            self.erase_img = None
            self.erase_text = 'Erase'
            self.erase_color = COLORS[8]

        try:
            self.clear_img = pygame.image.load('images/trash.png').convert_alpha()
            self.clear_img.set_colorkey(COLORS[0])
            self.clear_img = pygame.transform.scale(self.clear_img, (self.height, self.height))
            self.clear_text = ''
            self.clear_color = COLORS[0]
        except Exception as e:
            print(e)
            self.clear_img = None
            self.clear_text = 'Clear'
            self.clear_color = COLORS[8]

        try:
            self.filling_img = pygame.image.load('images/filling.png').convert_alpha()
            self.filling_img.set_colorkey(COLORS[0])
            self.filling_img = pygame.transform.scale(self.filling_img, (self.height, self.height))
            self.filling_text = ''
            self.filling_color = COLORS[0]
        except Exception as e:
            print(e)
            self.filling_img = None
            self.filling_text = 'Filling'
            self.filling_color = COLORS[8]

        self.filling_already_pressed = False
        self.erase_already_pressed = False
        self.old_draw_color = self.game.draw_color

        self.spec_buttons = ButtonArray(
            self.win,
            self.color_buttons.getWidth() + self.color_buttons.getX() + self.margin,
            self.y,
            int(self.width),
            self.height,
            (3, 1),
            border=0,
            colour=COLORS[0],
            inactiveColours=(self.erase_color, self.clear_color, self.filling_color),
            texts=(self.erase_text, self.clear_text, self.filling_text),
            images=(self.erase_img, self.clear_img, self.filling_img),
            onClicks=(self.erase_click, self.clear_click, self.filling_click),
        )

    def filling_click(self):
        if self.filling_already_pressed:
            self.game.board.filling = False
            self.filling_already_pressed = False
            self.spec_buttons.buttons[2].inactiveColour = self.filling_color
        else:
            self.game.board.filling = True
            self.filling_already_pressed = True
            self.spec_buttons.buttons[2].inactiveColour = self.spec_buttons.buttons[2].pressedColour
        self.game.connection.send({11: self.game.board.filling})

    def color_click(self):
        for color_button in self.color_buttons.buttons:
            if color_button.clicked:
                self.game.set_draw_color(color_button.inactiveColour)

    def erase_click(self):
        if self.erase_already_pressed:
            self.game.set_draw_color(self.old_draw_color)
            self.erase_already_pressed = False
            self.spec_buttons.buttons[0].inactiveColour = self.erase_color
        else:
            self.old_draw_color = self.game.draw_color
            self.game.set_draw_color(COLORS[0])
            self.erase_already_pressed = True
            self.spec_buttons.buttons[0].inactiveColour = self.spec_buttons.buttons[0].pressedColour

    def clear_click(self):
        self.game.board.clear()
        self.game.connection.send({9: []})
