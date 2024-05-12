import pygame
from field import Field


WINDOW_WIDTH = 0.66
WINDOW_HEIGHT = 0.74
CELL_X = 0.15625
CELL_Y = 0.25


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Создаю окно на весь экран

        self.display_size = self.window.get_size()  # Получаю размер экрана
        self.window_width = int(self.display_size[0] * WINDOW_WIDTH)
        self.window_height = int(self.display_size[1] * WINDOW_HEIGHT)
        self.window = pygame.display.set_mode((self.window_width, self.window_height))  # Создаю экран примерно 1280X800
        self.cell_size = self.get_cell_size()
        self.field = Field(self.window, self.cell_size)

    def run(self) -> None:
        while True:
            self.check_events()
            self.update_screen()

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update_screen(self) -> None:
        self.window.fill('gray')
        self.field.draw()
        pygame.display.update()

    def get_cell_size(self) -> tuple[int, int]:
        cell_x = int(self.window_width * CELL_X)
        cell_y = int(self.window_height * CELL_Y)
        return cell_x, cell_y


if __name__ == '__main__':
    game = Game()
    game.run()
