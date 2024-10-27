from player import Player


class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.players = []
        self.words_used = []
        self.round = None
        self.board = None

    def player_guess(self, player: Player, guess):
        pass

    def player_disconnect(self, player: Player):
        pass

    def skip(self):
        pass

    def round_ended(self):
        pass

    def update_board(self):
        pass
