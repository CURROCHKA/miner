import sys
import pygame


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Snake')

    def run(self):
        while True:
            self.check_events()
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_screen(self):
        self.screen.fill('gray')
        pygame.display.flip()


if __name__ == '__main__':
    snake_game = Game()
    snake_game.run()
