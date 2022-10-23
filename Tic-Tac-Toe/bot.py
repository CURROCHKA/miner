from random import choice


class Bot:
    def __init__(self, t_game):
        self.t_game = t_game
        self.buttons = self.t_game.buttons
        self.cross = self.t_game.cross
        self.zero = self.t_game.zero
        self.who = self.cross if self.t_game.who == self.zero else self.zero

    def chose_button(self):
        if self.t_game.check_field():
            empty_buttons = []
            for button in self.buttons:
                if button.status:
                    empty_buttons.append(button)
            return choice(empty_buttons)

    def make_move(self):
        empty_button = self.chose_button()
        for button in self.buttons:
            if button == empty_button:
                button.who = self.who
                button.status = False
        self.t_game.update_screen()
        self.t_game.victory_condition()
