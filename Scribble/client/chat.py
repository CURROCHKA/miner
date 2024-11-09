import pygame
from pygame_widgets.textbox import TextBox

from config import (
    COLORS,
    BORDER_THICKNESS,
    FONT_NAME,
)


class Chat:
    def __init__(self, win: pygame.Surface, x: float, y: float, width: int, height: int, margin: float, game):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = int(height / 20) * 19
        self.margin = margin
        self.game = game
        self.text_box_height = height - self.height
        self.content_gap = int(self.margin * 3)
        self.content = []
        self.font_size = int(self.width / 15)
        self.chat_font = pygame.font.SysFont(FONT_NAME, self.font_size)
        self.border_thickness = int(self.margin / BORDER_THICKNESS)
        self.text_box = TextBox(
            self.win,
            int(self.x - self.border_thickness / 2),
            int(self.y + self.height),
            int(self.width + self.border_thickness),
            int(self.text_box_height + self.border_thickness / 2),
            colour=COLORS[8],
            borderThickness=self.border_thickness,
            placeholderText='Write something',
            fontSize=self.font_size,
            font=self.chat_font,
            onSubmit=self.text_box_submit,
        )

    def text_box_submit(self):
        msg = self.text_box.getText()
        self.text_box.setText('')
        self.update_chat(msg)

    def update_chat(self, content):
        if isinstance(content, str):
            player_name, guess = self.game.connection.send({0: [content]})
            self.content = [(player_name, content, guess, False)]
        else:
            res = []
            for item in content:
                player_name, msg, is_sys_msg = item
                res.append((player_name, msg, False, is_sys_msg))
            self.content = res

    def draw(self):
        for i, content in enumerate(self.content):
            player_name, msg, guess, is_sys_msg = content

            bold = False
            text = f'{player_name}: {msg}'
            color = COLORS[7]

            if guess:
                color = COLORS[1]

            if is_sys_msg:
                bold = True
                text = msg

            self.chat_font.set_bold(bold)
            txt = self.chat_font.render(text, 1, color)
            self.chat_font.set_bold(False)
            self.win.blit(txt, (self.x + self.content_gap, self.y + self.content_gap / 2 + i * self.content_gap))

        pygame.draw.rect(self.win, COLORS[7], (self.x - self.border_thickness / 2,
                                               self.y - self.border_thickness / 2,
                                               self.width + self.border_thickness,
                                               self.height + self.border_thickness), self.border_thickness)
