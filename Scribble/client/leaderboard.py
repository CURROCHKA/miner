import pygame

from config import (
    COLORS,
    BORDER_THICKNESS,
    FONT_NAME,
)


class LeaderBoard:
    def __init__(self, win: pygame.Surface, x: float, y: float, width: int, height: int, margin: float):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height  # Высота одной строчки
        self.margin = margin
        self.text_color = COLORS[7]
        self.border_thickness = int(self.margin / BORDER_THICKNESS)
        self.players = []  # [(player: Player, name_font: pygame.font)]

        self.score_font_size = int(self.width / 15)
        self.score_font = pygame.font.SysFont(FONT_NAME, self.score_font_size)

        self.rank_font_size = int(self.height / 3)
        self.rank_font = pygame.font.SysFont(FONT_NAME, self.rank_font_size)

    def draw(self):
        scores = [(player[0].get_name(), player[0].get_score()) for player in self.players]
        scores.sort(key=lambda x: x[1], reverse=True)

        for i, player in enumerate(scores):
            name_font = self.players[i][1]
            if i % 2 == 0:
                color = COLORS[0]
            else:
                color = COLORS[8]
            pygame.draw.rect(self.win, color, (self.x, self.y + i * self.height, self.width, self.height))

            rank = self.rank_font.render(f'№ {i + 1}', 1, self.text_color)
            self.win.blit(rank, (self.x + self.margin,
                                 self.y + i * self.height + self.height / 2 - rank.get_height() / 2))

            name = name_font.render(player[0], 1, self.text_color)
            self.win.blit(name, (self.width / 3 + self.margin,
                                 self.y + i * self.height + self.height / 2 - name.get_height() / 2))

            score = self.score_font.render(f'Score: {player[1]}', 1, self.text_color)
            self.win.blit(score, (self.width / 3 + self.margin,
                                  self.y + i * self.height + (self.height - score.get_height()) - self.margin * 0.1))

        pygame.draw.rect(self.win, COLORS[7], (self.x - self.border_thickness / 2,
                                               self.y - self.border_thickness / 2,
                                               self.width + self.border_thickness,
                                               self.height * len(self.players) + self.border_thickness),
                         self.border_thickness)

    @staticmethod
    def __get_name_font(name: str, max_width: int, max_height: int):
        font_size = 1  # Начинаем с минимального размера
        font = pygame.font.SysFont(FONT_NAME, font_size)

        # Увеличиваем размер шрифта, пока текст не выйдет за границы
        while True:
            text_width, text_height = font.size(name)

            # Проверка, помещается ли текст по ширине или высоте
            if text_width > max_width or text_height > max_height:
                # print(text_width, text_height, font_size)
                font_size = min(text_width, text_height)  # Шаг назад, чтобы точно поместился текст
                break

            # Увеличиваем размер и создаем новый шрифт для проверки
            font_size += 1
            font = pygame.font.SysFont(FONT_NAME, font_size)
        return pygame.font.SysFont(FONT_NAME, font_size)

    def add_player(self, player):
        n = len(self.players) + 1
        name = player.get_name()
        rank = self.rank_font.render(f'№ {n}', 1, self.text_color)
        name_font = self.__get_name_font(name, self.width - rank.get_width() * 3, self.height)
        self.players.append((player, name_font))

    def remove_player(self, player):
        for p in self.players:
            if p[0] == player:
                self.players.remove(p)
                break
