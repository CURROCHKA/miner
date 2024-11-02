import pygame

from config import (
    COLORS,
    MAX_ROUND,
    BORDER_THICKNESS,
    FONT_NAME,
)


class TopBar:
    def __init__(self, win: pygame.Surface, x: float, y: float, width: int, height: int, margin: float):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = margin
        self.font_size = int(self.height / 2)
        self.word = ''
        self.round = 1
        self.color = COLORS[7]
        self.round_font = pygame.font.SysFont(FONT_NAME, self.font_size)
        self.border_thickness = int(self.margin / BORDER_THICKNESS)
        self.time = 75

    def draw(self):
        # draw round
        text = self.round_font.render(f'Round {self.round} of {MAX_ROUND}', 1, self.color)
        self.win.blit(text, (self.x + self.margin, self.y + self.height / 2 - text.get_height() / 2))

        # draw underscores
        text = self.round_font.render(self.underscore_text(self.word), 1, self.color)
        self.win.blit(text, (self.x + self.width / 2 - text.get_width() / 2,
                             self.y + self.height / 2 - text.get_height() / 2 + self.margin))

        pygame.draw.rect(self.win, COLORS[7], (self.x - self.border_thickness / 2,
                                               self.y - self.border_thickness / 2,
                                               self.width + self.border_thickness,
                                               self.height + self.border_thickness),
                         self.border_thickness)

        radius = self.height / 2
        pygame.draw.circle(self.win, COLORS[7], (int(self.x + self.width - radius),
                                                 int(self.y + self.height / 2)), radius, self.border_thickness)

        timer = self.round_font.render(str(self.time), 1, COLORS[7])
        self.win.blit(timer, (self.x + self.width - timer.get_width() / 2 - radius,
                              self.y + self.height / 2 - timer.get_height() / 2))

    @staticmethod
    def underscore_text(text: str):
        new_text = ''

        for char in text:
            if char != ' ':
                new_text += '_'
            else:
                new_text += ' '
        return new_text

    def change_word(self, word: str):
        self.word = word

    def change_round(self, rnd: int):
        self.round = rnd
