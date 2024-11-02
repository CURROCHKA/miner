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
            self.erase_img = pygame.image.load('Scribble/client/images/eraser.png').convert_alpha()
            self.erase_img.set_colorkey(COLORS[0])
            self.erase_img = pygame.transform.scale(self.erase_img, (int(self.width / 2), int(self.height / 2)))
            self.erase_text = ''
            self.erase_color = COLORS[0]
        except Exception as e:
            print(e)
            self.erase_img = None
            self.erase_text = 'Erase'
            self.erase_color = COLORS[8]

        try:
            self.clear_img = pygame.image.load('Scribble/client/images/trash.png').convert_alpha()
            self.clear_img.set_colorkey(COLORS[0])
            self.clear_img = pygame.transform.scale(self.clear_img, (int(self.width / 2), int(self.height / 2)))
            self.clear_text = ''
            self.clear_color = COLORS[0]
        except Exception as e:
            print(e)
            self.clear_img = None
            self.clear_text = 'Clear'
            self.clear_color = COLORS[8]

        self.erase_already_pressed = False
        self.old_draw_color = self.game.draw_color

        self.spec_buttons = ButtonArray(
            self.win,
            self.color_buttons.getWidth() + self.color_buttons.getX() + self.margin,
            self.y,
            int(self.width),
            self.height,
            (2, 1),
            border=0,
            colour=COLORS[0],
            inactiveColours=(self.erase_color, self.clear_color),
            texts=(self.erase_text, self.clear_text),
            images=(self.erase_img, self.clear_img),
            onClicks=(self.erase_click, self.clear_click),
        )

    def color_click(self):
        for color_button in self.color_buttons.buttons:
            if color_button.clicked:
                self.game.draw_color = color_button.inactiveColour

    def erase_click(self):
        if self.erase_already_pressed:
            self.game.set_draw_color(self.old_draw_color)
            self.erase_already_pressed = False
            self.spec_buttons.buttons[0].inactiveColour = COLORS[0]
        else:
            self.old_draw_color = self.game.draw_color
            self.game.set_draw_color(COLORS[0])
            self.erase_already_pressed = True
            self.spec_buttons.buttons[0].inactiveColour = self.spec_buttons.buttons[0].pressedColour

    def clear_click(self):
        self.game.board.clear()
