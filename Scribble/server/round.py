import time as t
from _thread import *

from player import Player
from game import Game
from chat import Chat


class Round:
    def __init__(self, word: str, player_drawing: Player, players: list[Player]):
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.skips = 0
        self.player_scores = {player: 0 for player in players}
        self.time = 75
        self.chat = Chat(self)
        self.start = t.time()
        start_new_thread(self.time_thread(), (conn, current_player))

    def time_thread(self):
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round('Time is up')

    def guess(self, player: Player, word: str) -> bool:
        correct = self.word == word
        if correct:
            self.player_guessed.append(player)

    def player_left(self, player: Player) -> None:
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove(player)

        if player == self.player_drawing:
            self.end_round('Drawing player leaves')

    def end_round(self, msg: str):
        pass
