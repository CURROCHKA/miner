from random import randint

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
    def __init__(self, game_id: int, players: list[Player]):
        self.id = game_id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = None
        self.player_draw_ind = 0
        self.round_count = 0
        self.start_new_round()
        self.create_board()

    def start_new_round(self) -> None:
        try:
            round_word = self.get_word()
            self.words_used.add(round_word)
            self.round = Round(self.get_word(), self.players[self.player_draw_ind], self)
            self.round_count += 1

            if self.player_draw_ind >= len(self.players):
                self.round_ended()
                self.end_game()

            self.player_draw_ind += 1
        except:
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

    def player_disconnected(self, player: Player):
        if player in self.players:
            player_ind = self.players.index(player)
            if player_ind >= self.player_draw_ind:
                self.player_draw_ind -= 1
            self.players.remove(player)
            self.round.player_left(player)
        else:
            raise Exception('Player not in game')

        if len(self.players) <= 2:
            self.end_game()

    def get_player_scores(self) -> dict[str, int]:
        scores = {player.name: player.get_score() for player in self.players}
        return scores

    def skip(self):
        if self.round:
            new_round = self.round.skip()
            if new_round:
                self.round_ended()
                return True
            return False
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
        print(f'[GAME] Game {self.id} ended')
        for player in self.players:
            player.game = None
            # self.round.player_left(player)

    def get_word(self) -> str:
        with open('Scribble/server/words.txt', 'r') as f:
            words = []

            for line in f:
                word = line.strip()
                if word not in self.words_used:
                    words.append(word)
            self.words_used.add(word)

            r = randint(0, len(words) - 1)
            return words[r]