import socket
import threading
import json

from player import Player
from game import Game
from config import (
    PLAYERS
)


class Server:
    def __init__(self):
        self.server = 'localhost'
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_queue = []
        self.game_id = 0

    def player_thread(self, connection, player: Player) -> None:
        while True:
            try:
                try:
                    data = connection.recv(1024)
                    data = json.loads(data.decode())
                except Exception as e:
                    print(f'[EXCEPTION] {e}')
                    break

                keys = [int(key) for key in data.keys()]
                send_msg = {key: [] for key in keys}
                last_board = None

                for key in keys:
                    if key == -1:  # get a list of players
                        if player.game:
                            send = [player.get_name() for player in player.game.players]
                            send_msg[-1] = send
                        else:
                            send_msg[-1] = []

                    if player.game:
                        if key == 0:  # guess
                            correct = player.game.player_guess(player, data['0'][0])
                            send_msg[0] = [player.get_name(), correct]

                        elif key == 1:  # skip
                            skip = player.game.skip(player)
                            send_msg[1] = skip

                        elif key == 2:  # get chat
                            content = player.game.round.chat.get_chat()
                            send_msg[2] = content

                        elif key == 3:  # get board
                            board = player.game.board.get_board()
                            if last_board != board:
                                last_board = board
                                send_msg[3] = board

                        elif key == 4:  # get score
                            scores = player.game.get_player_scores()
                            send_msg[4] = scores

                        elif key == 5:  # get round
                            rnd = player.game.round_count
                            send_msg[5] = rnd

                        elif key == 6:  # get word
                            word = player.game.round.get_word()
                            send_msg[6] = word

                        elif key == 7:  # update board
                            if player.game.round.player_drawing == player:
                                x, y, color = data['7'][:3]
                                player.game.update_board(x, y, color)

                        elif key == 8:  # get round time
                            t = player.game.round.time
                            send_msg[8] = t

                        elif key == 9:  # clear board
                            if player.game.round.player_drawing == player:
                                player.game.board.clear()

                        elif key == 10:  # get is_drawing_player
                            send_msg[10] = player.game.round.player_drawing == player

                send_msg = json.dumps(send_msg)
                connection.sendall(send_msg.encode())

            except Exception as e:
                print(f'[EXCEPTION] {player.get_name()}: {e}')
                break

        if player.game:
            player.game.player_disconnected(player)

        if player in self.connection_queue:
            self.connection_queue.remove(player)

        print(f'[DISCONNECT] {player.get_name()} disconnected')
        connection.close()

    def handle_queue(self, player: Player) -> None:
        self.connection_queue.append(player)

        if len(self.connection_queue) >= PLAYERS:
            game = Game(self.game_id, self.connection_queue[:])

            for player in game.players:
                player.set_game(game)

            self.game_id += 1
            self.connection_queue = []
            print(f'[GAME] Game {self.game_id - 1} started')

    def authentication(self, connection, address) -> None:
        try:
            data = connection.recv(1024)
            name = str(data.decode())
            if not name:
                raise Exception('No name received')

            connection.sendall('1'.encode())
            player = Player(address, name)
            self.handle_queue(player)
            thread = threading.Thread(target=self.player_thread, args=(connection, player))
            thread.start()
        except Exception as e:
            print(f'[EXCEPTION] {e}')
            connection.close()

    def connection_thread(self) -> None:
        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.socket.listen(1)
        print('Waiting for a connection, Server started')

        while True:
            connection, address = self.socket.accept()
            print('[CONNECT] New connection')
            self.authentication(connection, address)


if __name__ == '__main__':
    server = Server()
    thread = threading.Thread(target=server.connection_thread)
    thread.start()
