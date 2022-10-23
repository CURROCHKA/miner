import sys
from time import sleep
from random import choice
import pygame
from settings import Settings
from field import Field
from button import Button
from zero import Zero
from cross import Cross
from bot import Bot
from message import Message


class TicTacToe:
    """Основной класс игры."""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1280, 800))
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        pygame.display.set_caption('Tic-Tac_Toe')
        self.zero = Zero(self)
        self.cross = Cross(self)
        self.who = choice((self.zero, self.cross))
        self.field = Field(self)
        self.buttons = {
            'topleft': pygame.Rect(446, 205, 125, 125),
            'top': pygame.Rect(577, 205, 125, 125),
            'topright': pygame.Rect(705, 205, 125, 125),
            'left': pygame.Rect(446, 336, 125, 125),
            'center': pygame.Rect(577, 336, 125, 125),
            'right': pygame.Rect(705, 336, 125, 125),
            'bottomleft': pygame.Rect(446, 466, 125, 125),
            'bottom': pygame.Rect(577, 466, 125, 125),
            'bottomright': pygame.Rect(705, 466, 125, 125)
        }
        self.buttons = [Button(self, button, self.buttons[button]) for button in self.buttons]
        self.bot = Bot(self)

    def run_game(self):
        """Основной цикл игры."""
        while self.check_field():
            self.check_events()
            self.update_screen()

    def check_field(self):
        empty_buttons = [button for button in self.buttons if button.status]
        if empty_buttons:
            return True
        return False

    def whose_move(self):
        self.update_screen()
        self.victory_condition()
        if self.who == self.cross:
            self.who = self.zero
        else:
            self.who = self.cross
        if self.who == self.bot.who:
            self.bot.make_move()
            self.who = self.cross if self.who == self.zero else self.zero

    def victory_condition(self):
        win_pos = (('topleft', 'top', 'topright'),
                   ('left', 'center', 'right'),
                   ('bottomleft', 'bottom', 'bottomright'),
                   ('topleft', 'left', 'bottomleft'),
                   ('top', 'center', 'bottom'),
                   ('topright', 'right', 'bottomright'),
                   ('topleft', 'center', 'bottomright'),
                   ('topright', 'center', 'bottomleft'),)

        for pos in win_pos:
            if [True for button in self.buttons if button.name == pos[0] and button.who == self.who] and \
                    [True for button in self.buttons if button.name == pos[1] and button.who == self.who] and \
                    [True for button in self.buttons if button.name == pos[2] and button.who == self.who]:
                self.who_win()
                sleep(1)
                sys.exit()

    def who_win(self):
        if self.who is self.zero:
            message = Message(self, 'Выиграл Нолик!')
            print('Выиграл Нолик!')
        else:
            message = Message(self, 'Выиграл Крестик!')
            print('Выиграл Крестик!')
        message.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_q:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_mouse_events(mouse_pos)

    def check_mouse_events(self, mouse_pos):
        button_clicked = {}
        for button in self.buttons:
            button_clicked.update({button: button.rect.collidepoint(mouse_pos)})

        for button in button_clicked:
            if button_clicked[button] and button.status:
                button.who = self.who
                button.status = False
                self.whose_move()
                break

    def buttons_update(self):
        for button in self.buttons:
            if not button.status:
                if button.who == self.zero:
                    self.screen.blit(self.zero.image, button.rect)
                else:
                    self.screen.blit(self.cross.image, button.rect)

    def update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.screen_color)
        self.field.update()
        [button.draw_button() for button in self.buttons]
        self.buttons_update()
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    t_game = TicTacToe()
    t_game.run_game()
