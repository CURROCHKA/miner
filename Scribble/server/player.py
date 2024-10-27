class Player:
    def __init__(self, ip, name):
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0

    def update_score(self, score: int):
        self.score += score

    def guess(self):
        pass

    def disconnect(self):
        pass

    def get_ip(self):
        return self.ip

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score