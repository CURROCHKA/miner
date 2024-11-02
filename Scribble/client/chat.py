import pygame
from pygame_widgets.textbox import TextBox

from config import (
    COLORS,
    BORDER_THICKNESS,
    FONT_NAME,
    CHAT_FONT_SIZE,
)


class Chat:
    def __init__(self, win: pygame.Surface, x: float, y: float, width: int, height: int, margin: float):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = int(height / 20) * 19
        self.margin = margin
        self.text_box_height = height - self.height
        self.content_gap = int(self.margin * 3)
        self.content = ['HEllo', 'qwqw', 'qqq']
        self.font_size = int(self.width / CHAT_FONT_SIZE)
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
            onSubmit=self.text_box_submit,
        )

    def text_box_submit(self):
        msg = self.text_box.getText()
        self.text_box.setText('')
        self.update_chat(msg)

    def update_chat(self, msg: str):
        self.content.append(msg)

    def draw(self):
        while len(self.content) * self.content_gap > self.height - 100:
            self.content = self.content[:-1]
        for i, msg in enumerate(self.content):
            txt = self.chat_font.render(f': {msg}', 1, COLORS[7])
            self.win.blit(txt, (self.x + self.content_gap, self.y + self.content_gap / 2 + i * self.content_gap))

        pygame.draw.rect(self.win, COLORS[7], (self.x - self.border_thickness / 2,
                                               self.y - self.border_thickness / 2,
                                               self.width + self.border_thickness,
                                               self.height + self.border_thickness), self.border_thickness)
