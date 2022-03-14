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
            self.victory_condition()
            self.update_screen()

    def whose_move(self):
        if self.who == self.cross:
            self.who = self.zero
        else:
            self.who = self.cross

    def victory_condition(self):

        if self.settings.topleft_who == self.who \
                and self.settings.top_who == self.who \
                and self.settings.topright_who == self.who:
            sleep(5)
            sys.exit()

        if self.settings.topleft_who == self.who \
                and self.settings.left_who == self.who \
                and self.settings.bottomleft_who == self.who:
            sleep(5)
            sys.exit()

        if self.settings.topleft_who == self.who \
                and self.settings.center_who == self.who \
                and self.settings.bottomright_who == self.who:
            sleep(5)
            sys.exit()

        if self.settings.top_who == self.who \
                and self.settings.center_who == self.who \
                and self.settings.bottom_who == self.who:
            sleep(5)
            sys.exit()

        if self.settings.topright_who == self.who \
                and self.settings.center_who == self.who \
                and self.settings.bottomleft_who == self.who:
            sleep(5)
            sys.exit()

        if self.settings.right_who == self.who \
                and self.settings.center_who == self.who \
                and self.settings.left_who == self.who:
            sleep(5)
            sys.exit()

        if self.settings.bottomleft_who == self.who \
                and self.settings.bottom_who \
                and self.settings.bottomright_who == self.who:
            sleep(5)
            sys.exit()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_q:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_mouse_events(mouse_pos)

    def check_mouse_events(self, mouse_pos):

        topleft_clicked = self.buttons['topleft_button'].button_rect.collidepoint(mouse_pos)
        top_clicked = self.buttons['top_button'].button_rect.collidepoint(mouse_pos)
        topright_clicked = self.buttons['topright_button'].button_rect.collidepoint(mouse_pos)
        left_clicked = self.buttons['left_button'].button_rect.collidepoint(mouse_pos)
        center_clicked = self.buttons['center_button'].button_rect.collidepoint(mouse_pos)
        right_clicked = self.buttons['right_button'].button_rect.collidepoint(mouse_pos)
        bottomleft_clicked = self.buttons['bottomleft_button'].button_rect.collidepoint(mouse_pos)
        bottom_clicked = self.buttons['bottom_button'].button_rect.collidepoint(mouse_pos)
        bottomright_clicked = self.buttons['bottomright_button'].button_rect.collidepoint(mouse_pos)

        # Topleft button
        if topleft_clicked and self.settings.topleft_active:
            self.settings.topleft_who = self.who
            self.whose_move()
            self.settings.topleft_active = False

        # Center button
        if center_clicked and self.settings.center_active:
            self.settings.center_who = self.who
            self.whose_move()
            self.settings.center_active = False

        # Topright button
        if topright_clicked and self.settings.topright_active:
            self.settings.topright_who = self.who
            self.whose_move()
            self.settings.topright_active = False

        # Top button
        if top_clicked and self.settings.top_active:
            self.settings.top_who = self.who
            self.whose_move()
            self.settings.top_active = False

        # Left button
        if left_clicked and self.settings.left_active:
            self.settings.left_who = self.who
            self.whose_move()
            self.settings.left_active = False

        # Bottomleft button
        if bottomleft_clicked and self.settings.bottomleft_active:
            self.settings.bottomleft_who = self.who
            self.whose_move()
            self.settings.bottomleft_active = False

        # Bottom button
        if bottom_clicked and self.settings.bottom_active:
            self.settings.bottom_who = self.who
            self.whose_move()
            self.settings.bottom_active = False

        # Bottomright button
        if bottomright_clicked and self.settings.bottomright_active:
            self.settings.bottomright_who = self.who
            self.whose_move()
            self.settings.bottomright_active = False

        # Right button
        if right_clicked and self.settings.right_active:
            self.settings.right_who = self.who
            self.whose_move()
            self.settings.right_active = False

    def buttons_update(self):

        # Topleft button
        if not self.settings.topleft_active:
            if self.settings.topleft_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['topleft_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['topleft_button'].button_rect)

        # Top button
        if not self.settings.top_active:
            if self.settings.top_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['top_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['top_button'].button_rect)

        # Topright button
        if not self.settings.topright_active:
            if self.settings.topright_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['topright_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['topright_button'].button_rect)

        # Left button
        if not self.settings.left_active:
            if self.settings.left_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['left_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['left_button'].button_rect)

        # Center button
        if not self.settings.center_active:
            if self.settings.center_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['center_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['center_button'].button_rect)

        # Right button
        if not self.settings.right_active:
            if self.settings.right_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['right_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['right_button'].button_rect)

        # Bottomleft button
        if not self.settings.bottomleft_active:
            if self.settings.bottomleft_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['bottomleft_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['bottomleft_button'].button_rect)

        # Bottom button
        if not self.settings.bottom_active:
            if self.settings.bottom_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['bottom_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['bottom_button'].button_rect)

        # Bottomright button
        if not self.settings.bottomright_active:
            if self.settings.bottomright_who == self.zero:
                self.screen.blit(self.zero.image, self.buttons['bottomright_button'].button_rect)
            else:
                self.screen.blit(self.cross.image, self.buttons['bottomright_button'].button_rect)

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
