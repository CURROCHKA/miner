import json

class GameStats:
    """Отслеживание статистики для игры."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()
        try:
            with open('high_score.json') as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0
        # Игра запускается в неактивном состоянии
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1