import time as t
from _thread import *

from player import Player
from chat import Chat


class Round:
    def __init__(self, word: str, player_drawing: Player, game):
        self.word = word
        self.player_drawing = player_drawing
        self.game = game
        self.player_scores = {player: 0 for player in self.game.players}
        self.players_guessed = []
        self.players_skipped = []
        self.skips = 0
        self.time = 75
        self.chat = Chat(self)
        self.start = t.time()
        start_new_thread(self.time_thread, ())

    def skip(self, player) -> bool:
        if player not in self.players_skipped:
            self.players_skipped.append(player)
            self.skips += 1
            self.chat.update_chat('',
                                  f'Player has votes to skip ({self.skips}/{len(self.game.players) - 2}',
                                  True)
            return self.skips >= len(self.game.players) - 2
        return False

    def get_scores(self):
        return self.player_scores

    def get_score(self, player: Player):
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception('Player not in score list')

    def time_thread(self):
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round('Time is up')

    def guess(self, player: Player, msg: str) -> bool:
        correct = self.word.lower() == msg.lower()
        if correct:
            self.players_guessed.append(player)
            self.chat.update_chat('', f'{player.get_name()} has guessed the word', True)
            return True
        self.chat.update_chat(player.get_name(), msg, False)
        return False

    def player_left(self, player: Player) -> None:
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.players_guessed:
            self.players_guessed.remove(player)

        if player == self.player_drawing:
            self.chat.update_chat('', f'Round has been skipped because the drawer left', True)
            self.end_round('Drawing player leaves')

    def end_round(self, msg: str):
        for player in self.game.players:
            if player in self.player_scores:
                player.update_score(self.player_scores[player])
        self.game.round_ended()
