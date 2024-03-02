import sys
import pygame
from snake import Snake


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.snake = Snake(self.screen_rect)
        self.clock = pygame.time.Clock()
        self.frame = 5
        pygame.display.set_caption('Snake')

    def run(self):
        while True:
            self.check_events()
            self.snake.update()
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.__check_keydown_events(event)

    def __check_keydown_events(self, event: pygame.event):
        key = event.key
        directions = {
            pygame.K_w: (0, -1),
            pygame.K_UP: (0, -1),
            pygame.K_a: (-1, 0),
            pygame.K_LEFT: (-1, 0),
            pygame.K_s: (0, 1),
            pygame.K_DOWN: (0, 1),
            pygame.K_d: (1, 0),
            pygame.K_RIGHT: (1, 0)
        }

        if key in directions and self.snake.speed != 0:
            dx, dy = directions[key]
            if (dx, dy) != (-self.snake.moving_x, -self.snake.moving_y):
                self.snake.moving_x, self.snake.moving_y = dx, dy

    def update_screen(self):
        self.screen.fill('gray')
        self.snake.draw(self.screen)
        self.clock.tick(self.frame)
        pygame.display.flip()


if __name__ == '__main__':
    snake_game = Game()
    snake_game.run()
