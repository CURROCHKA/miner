from player import Player
from board import Board
from round import Round
from config import (
    WIDTH,
    HEIGHT,
    HORIZONTAL_MARGIN,
    VERTICAL_MARGIN,
    GRID_SIZE
)


class Game:
    def __init__(self, game_id: int, thread):
        self.id = game_id
        self.players = []
        self.words_used = []
        self.round = None
        self.board = None
        self.player_draw_ind = 0
        self.connected_thread = thread
        self.start_new_round()
        self.create_board()

    def start_new_round(self) -> None:
        self.round = Round(self.get_word(), self.players[self.player_draw_ind], self.players, self)
        self.player_draw_ind += 1

        if self.player_draw_ind >= len(self.players):
            self.round.end_round('')
            self.end_game()

    def create_board(self):
        horizontal_margin = WIDTH / HORIZONTAL_MARGIN
        vertical_margin = HEIGHT / VERTICAL_MARGIN
        cell_size = (
            (WIDTH - horizontal_margin * 2) / GRID_SIZE[0],
            (HEIGHT - vertical_margin) / GRID_SIZE[1]
        )
        self.board = Board(x=horizontal_margin,
                           y=vertical_margin,
                           grid_size=GRID_SIZE,
                           cell_size=cell_size)

    def player_guess(self, player: Player, word: str):
        return self.round.guess(player, word)

    def player_disconnect(self, player: Player):
        pass

    def skip(self):
        if self.round:
            new_round = self.round.skip()
            if new_round:
                self.round_ended()
        else:
            raise Exception('No round started yet!')

    def round_ended(self):
        self.start_new_round()
        self.board.clear()

    def update_board(self, x: int, y: int, color: tuple[int, int, int]):
        if self.board:
            self.board.update(x, y, color)
        else:
            raise Exception('No board created')

    def end_game(self):
        pass

    def get_word(self) -> str:
        pass
