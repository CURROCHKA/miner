from random import choice
import traceback

from player import Player
from board import Board
from round import Round


class Game:
    def __init__(self, game_id: int, players: list[Player]):
        self.id = game_id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 0
        self.start_new_round()

    def start_new_round(self) -> None:
        try:
            chat_content = []
            if self.round:
                chat_content = self.round.chat.get_chat()
            self.round = Round(self.get_new_word(), self.players[self.player_draw_ind], self)
            self.round_count += 1
            self.round.chat.content = chat_content

            if self.player_draw_ind >= len(self.players):
                self.round_ended()
                self.end_game()

            self.player_draw_ind += 1
        except Exception as e:
            print(f'[EXCEPTION] {e}')
            traceback.print_exc()
            self.end_game()

    def player_guess(self, player: Player, word: str):
        return self.round.guess(player, word)

    def player_disconnected(self, player: Player):
        if player in self.players:
            self.players.remove(player)
            self.round.player_left(player)
            self.round.chat.update_chat('', f'Player {player.get_name()} disconnected', True)
        else:
            raise Exception('Player not in game')

        if len(self.players) <= 2:
            self.end_game()

    def get_player_scores(self) -> dict[str, int]:
        scores = {player.get_name(): player.get_score() for player in self.players}
        return scores

    def skip(self, player):
        if self.round:
            new_round = self.round.skip(player)
            if new_round:
                self.round.chat.update_chat('', 'Round has been skipped', True)
                self.round_ended()
                return True
            return False
        else:
            raise Exception('No round started yet!')

    def round_ended(self):
        self.round.chat.update_chat('', f'Round {self.round_count} has ended', True)
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

    def get_new_word(self) -> str:
        try:
            with open('Scribble/server/words.txt', 'r') as f:
                words = []

                for line in f:
                    word = line.strip()
                    if word not in self.words_used:
                        words.append(word)

                wrd = choice(words)
                self.words_used.add(wrd)
                return wrd
        except Exception as e:
            print(f'[EXCEPTION] {e}')
            self.end_game()
