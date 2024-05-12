import sys
from time import sleep
from random import choice
import pygame

from settings import Settings
from field import Field
from button import Button
from zero import Zero
from cross import Cross


class TicTacToe:
    """Основной класс игры."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        # Экран
        self.screen = pygame.display.set_mode((1280, 800))
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        pygame.display.set_caption('Tic-Tac_Toe')

        self.zero = Zero(self)
        self.cross = Cross(self)
        self.who = choice((self.zero, self.cross))
        self.field = Field(self)

        self.buttons = {'topleft_button': Button(self, 446, 205, 125, 125),
                        'top_button': Button(self, 577, 205, 125, 125),
                        'topright_button': Button(self, 705, 205, 125, 125),
                        'left_button': Button(self, 446, 336, 125, 125),
                        'center_button': Button(self, 577, 336, 125, 125),
                        'right_button': Button(self, 705, 336, 125, 125),
                        'bottomleft_button': Button(self, 446, 466, 125, 125),
                        'bottom_button': Button(self, 577, 466, 125, 125),
                        'bottomright_button': Button(self, 705, 466, 125, 125)
                        }

    def run_game(self):
        """Основной цикл игры."""
        while True:
            self.check_events()
            self.update_screen()

    def whose_move(self):
        if self.who == self.cross:
            self.who = self.zero
        else:
            self.who = self.cross

    def victory_condition(self):
        win_positions = [[self.buttons['topleft_button'].who, self.buttons['top_button'].who, self.buttons['topright_button'].who],
                         [self.buttons['left_button'].who, self.buttons['center_button'].who, self.buttons['right_button'].who],
                         [self.buttons['bottomleft_button'].who, self.buttons['bottom_button'].who, self.buttons['bottomright_button'].who],
                         [self.buttons['topleft_button'].who, self.buttons['left_button'].who, self.buttons['bottomleft_button'].who],
                         [self.buttons['top_button'].who, self.buttons['center_button'].who, self.buttons['bottom_button'].who],
                         [self.buttons['topright_button'].who, self.buttons['center_button'].who, self.buttons['bottomleft_button'].who],
                         [self.buttons['topleft_button'].who, self.buttons['center_button'].who, self.buttons['bottomright_button'].who],
                         [self.buttons['topright_button'].who, self.buttons['center_button'].who, self.buttons['bottomleft_button'].who]]
        my_positions = []

        for positions in win_positions:
            for position in positions:
                if position == self.who:
                    my_positions.append(position)
                    if my_positions in win_positions:
                        sys.exit()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_q:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_mouse_events(mouse_pos)

    def check_mouse_events(self, mouse_pos):
        for i in self.buttons:
            if self.buttons[i].rect.collidepoint(mouse_pos) and self.buttons[i].button_active:
                self.buttons[i].who = self.who
                self.whose_move()
                self.buttons[i].button_active = False

    def buttons_update(self):
        for i in self.buttons:
            if not self.buttons[i].button_active:
                if self.buttons[i].who == self.zero:
                    self.screen.blit(self.zero.image, self.buttons[i].rect)
                else:
                    self.screen.blit(self.cross.image, self.buttons[i].rect)

    def update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.screen_color)
        self.field.update()
        for button in self.buttons:
            self.buttons[button].draw_button()
        self.buttons_update()

        pygame.display.flip()


if __name__ == '__main__':
    t_game = TicTacToe()
    t_game.run_game()
