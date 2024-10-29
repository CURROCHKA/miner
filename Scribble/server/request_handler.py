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
        self.connection_queue = []
        self.game_id = 0

    def player_thread(self, connection, player: Player) -> None:
        while True:
            try:
                try:
                    data = connection.recv(1024)
                    data = json.loads(data.decode())
                    print(f'[LOG] Received data: {data}')
                except:
                    break

                keys = [int(key) for key in data.keys()]
                send_msg = {key: [] for key in keys}

                for key in keys:
                    if key == -1:  # get game, returns a list of players
                        if player.game:
                            send = {player.get_name(): player.get_score() for player in player.game.players}
                            send_msg[-1] = [send]
                        else:
                            send_msg[-1] = []

                    if player.game:
                        if key == 0:  # guess
                            correct = player.game.player_guess(player, data['0'][0])
                            send_msg[0] = correct

                        elif key == 1:  # skip
                            skip = player.game.skip()
                            send_msg[1] = skip

                        elif key == 2:  # get chat
                            content = player.game.round.chat.get_chat()
                            send_msg[2] = content

                        elif key == 3:  # get board
                            board = player.game.board.get_board()
                            send_msg[3] = board

                        elif key == 4:  # get score
                            scores = player.game.get_player_scores()
                            send_msg[4] = scores

                        elif key == 5:  # get round
                            rnd = player.game.round_count
                            send_msg[5] = rnd

                        elif key == 6:  # get word
                            word = player.game.get_word()
                            send_msg[6] = word

                        elif key == 7:  # get skips
                            skips = player.game.round.skips
                            send_msg[7] = skips

                        elif key == 8:  # update board
                            x, y, color = data[8][:3]
                            player.game.update_board(x, y, color)

                        elif key == 9:  # get round time
                            t = player.game.round.time
                            send_msg[9] = t

                send_msg = json.dumps(send_msg)
                connection.sendall(send_msg.encode())

            except Exception as e:
                print(f'[EXCEPTION] {player.get_name()}: {e}')
                break

        print(f'[DISCONNECT] {player.get_name()} disconnected')
        # player.game.player_disconnected(player)
        connection.close()

    def handle_queue(self, player: Player) -> None:
        self.connection_queue.append(player)

        if len(self.connection_queue) >= PLAYERS:
            game = Game(self.game_id, self.connection_queue)

            for player in self.connection_queue:
                player.set_game(game)

            self.game_id += 1
            self.connection_queue = []

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
        server = 'localhost'
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen()
        print('Waiting for a connection, Server started')

        while True:
            connection, address = s.accept()
            print('[CONNECT] New connection')

            self.authentication(connection, address)


if __name__ == '__main__':
    s = Server()
    thread = threading.Thread(target=s.connection_thread)
    thread.start()
