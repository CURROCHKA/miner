from round import Round


class Chat:
    def __init__(self, rnd: Round):
        self.content = []
        self.round = rnd

    def update_chat(self, msg: str) -> None:
        self.content.append(msg)

    def get_chat(self):
        return self.content

    def __len__(self):
        return len(self.content)

    def __str__(self):
        return ''.join(self.content)

    def __repr__(self):
        return str(self)

