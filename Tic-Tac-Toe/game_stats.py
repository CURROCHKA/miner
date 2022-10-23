import sys


class GameStats:
    def __init__(self, t_game):
        self.buttons = t_game.buttons
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.topleft_active = True
        self.topleft_who = ''

        self.center_active = True
        self.center_who = ''

        self.topright_active = True
        self.topright_who = ''

        self.top_active = True
        self.top_who = ''

        self.left_active = True
        self.left_who = ''

        self.bottomleft_active = True
        self.bottomleft_who = ''

        self.bottom_active = True
        self.bottom_who = ''

        self.bottomright_active = True
        self.bottomright_who = ''

        self.right_active = True
        self.right_who = ''
