class Chat:
    def __init__(self, rnd):
        self.content = []
        self.round = rnd

    def update_chat(self, player_name, msg: str, is_sys_msg: bool) -> None:
        self.content.append((player_name, msg, is_sys_msg))

    def get_chat(self):
        return self.content

    def __len__(self):
        return len(self.content)

    def __str__(self):
        return ''.join(self.content)

    def __repr__(self):
        return str(self)
