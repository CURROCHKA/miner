import socket
import threading
import json
import zlib
import traceback

from Scribble.server.player import Player
from Scribble.server.game import Game
from config import (
    PLAYERS,
)


class Server:
    def __init__(self):
        self.server = 'localhost'
        self.port = 5555
        self.connection_queue = []
        self.game_id = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.server, self.port))
        self.socket.listen(32)

    def player_thread(self, connection: socket.socket, player: Player) -> None:
        while True:
            try:
                data = connection.recv(2048)
                if not data:
                    break

                data = json.loads(data.decode())
                keys = list(map(int, data.keys()))
                send_msg = {key: [] for key in keys}

                for key in keys:
                    if key == -1:  # get a list of players
                        if player.game:
                            send_msg[-1] = [player.get_name() for player in player.game.players]
                        else:
                            send_msg[-1] = []

                    if player.game:
                        if key == 0:  # guess
                            correct = player.game.player_guess(player, data['0'][0])
                            send_msg[0] = [player.get_name(), correct]

                        elif key == 1:  # skip
                            send_msg[1] = player.game.skip(player)

                        elif key == 2:  # get chat
                            send_msg[2] = player.game.round.chat.get_chat()

                        elif key == 3:  # get board
                            board = player.game.board.get_board()
                            send_msg[3] = board

                        elif key == 4:  # get score
                            send_msg[4] = player.game.get_player_scores()

                        elif key == 5:  # get round
                            send_msg[5] = player.game.round_count

                        elif key == 6:  # get word
                            send_msg[6] = player.game.round.get_word()

                        elif key == 7:  # update board
                            if player.game.round.player_drawing == player:
                                x, y, color = data['7']
                                player.game.update_board(x, y, color)

                        elif key == 8:  # get round time
                            send_msg[8] = player.game.round.time

                        elif key == 9:  # clear board
                            player.game.board.clear()

                        elif key == 10:  # get is_drawing_player
                            send_msg[10] = player.game.round.player_drawing == player

                        elif key == 11:  # set filling in board
                            filling = data['11']
                            player.game.board.filling = filling

                send_msg = json.dumps(send_msg)
                compressed_data = zlib.compress(send_msg.encode())
                connection.sendall(len(compressed_data).to_bytes(4, 'big'))
                connection.sendall(compressed_data)

            except Exception as e:
                print(f'[EXCEPTION] {player.get_name()}: {e}')
                traceback.print_exc()
                break

        self.disconnect(connection, player)

    def disconnect(self, connection: socket.socket, player: Player) -> None:
        if player.game:
            player.game.player_disconnected(player)

        if player in self.connection_queue:
            self.connection_queue.remove(player)

        print(f'[DISCONNECT] {player.get_name()} disconnected')
        # connection.sendall(player.get_name().encode())
        connection.close()

    def handle_queue(self, player: Player) -> None:
        self.connection_queue.append(player)

        if len(self.connection_queue) >= PLAYERS:
            game = Game(self.game_id, self.connection_queue[:PLAYERS])

            for player in game.players:
                player.set_game(game)

            self.game_id += 1
            self.connection_queue = self.connection_queue[PLAYERS:]
            print(f'[GAME] Game {self.game_id - 1} started')

    def authentication(self, connection: socket.socket, address: tuple[str, int]) -> None:
        try:
            data = connection.recv(1024)
            name = str(data.decode()).strip()
            if not name:
                raise ValueError('No name received')
            elif name in [player.get_name() for player in self.connection_queue]:
                connection.sendall('-1'.encode())
                raise ValueError('This nickname already exist')

            connection.sendall('1'.encode())
            player = Player(address, name)
            self.handle_queue(player)
            thread = threading.Thread(target=self.player_thread, args=(connection, player))
            thread.start()
        except Exception as e:
            print(f'[EXCEPTION] Error authenticating player {address}: {e}')
            connection.close()

    def connection_thread(self) -> None:
        try:
            print('Server started, waiting for connections...')

            while True:
                connection, address = self.socket.accept()
                print(f'[CONNECT] New connection from {address}')
                self.authentication(connection, address)

        except socket.error as e:
            print(f'[ERROR] {e}')
            self.socket.close()


if __name__ == '__main__':
    server = Server()
    thread = threading.Thread(target=server.connection_thread)
    thread.start()
