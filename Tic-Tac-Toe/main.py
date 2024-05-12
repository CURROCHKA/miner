import pygame


WINDOW_WIDTH = 0.66
WINDOW_HEIGHT = 0.74


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_size = self.window.get_size()
        self.width = self.screen_size[0] * WINDOW_WIDTH
        self.height = self.screen_size[1] * WINDOW_HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))

    def run(self):
        while True:
            self.check_events()
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update_screen(self):
        self.window.fill('gray')
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
