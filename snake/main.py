import sys
import pygame
from random import randrange
from snake import Snake
from fruit import Fruit


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_size = self.screen.get_size()
        self.font_style = pygame.font.SysFont('consolas', int(self.screen_rect.w * 0.045))
        self.cell_size = (round(self.screen_size[0] * 0.013), round(self.screen_size[1] * 0.0231))
        self.snake = Snake(self.create_snake_coord(), self.cell_size)
        self.fruit = Fruit(self.create_fruit_coord(), self.cell_size)
        self.clock = pygame.time.Clock()
        self.frame = 5
        self.score = 0
        pygame.display.set_caption('Snake')

    def run(self):
        while True:
            if self.snake.check_collisions():
                pygame.quit()
                sys.exit()
            self.check_events()
            self.snake.update(self.screen_rect)
            self.update_screen()

    def create_snake_coord(self) -> tuple:
        x = int(self.screen_rect.centerx - self.screen_rect.centerx % self.cell_size[0])
        y = int(self.screen_rect.centery - self.screen_rect.centery % self.cell_size[1])
        return x, y

    def create_fruit_coord(self) -> tuple:
        space_x = int(self.screen_size[0] - self.screen_size[0] % self.cell_size[0])
        space_y = int(self.screen_size[1] - self.screen_size[1] % self.cell_size[1])

        def generate_coord():
            x = randrange(0, space_x, self.cell_size[0])
            y = randrange(0, space_y, self.cell_size[1])
            return x, y

        while True:
            coord = generate_coord()
            if coord not in self.snake.snake_list:
                return coord

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

        if (self.snake.x, self.snake.y) == (self.fruit.x, self.fruit.y):
            self.snake.len += 1
            self.score += 1
            self.fruit.x, self.fruit.y = self.create_fruit_coord()
            self.frame += 1 if self.frame <= 15 and self.score % 3 == 0 else 0  # Увеличение скорости игры

    def check_keydown_events(self, event: pygame.event):
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
            self.snake.direction_buffer.append((dx, dy))

    def print_message(self, msg: str, color: str, pos: tuple):
        print_msg = self.font_style.render(msg, True, color)
        msg_rect = print_msg.get_rect()
        msg_rect.center = pos
        self.screen.blit(print_msg, msg_rect)

    def update_screen(self):
        self.screen.fill('gray')
        self.print_message(f'Score {self.score}', 'yellow', (self.screen_rect.centerx, self.screen_rect.h * 0.04))
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.frame)


if __name__ == '__main__':
    snake_game = Game()
    snake_game.run()
