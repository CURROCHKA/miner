import sys
import pygame
from ruby import Ruby
from random import choice

COLORS = ['blue', 'green', 'purple', 'red', 'yellow']


class Rubies:
    def __init__(self): # Иницицализация
        pygame.init()

        self.WIDTH, self.HEIGHT = 1200, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.rubies = []
        self.rubies_simple = []
        self.number_rows, self.number_rubies_x = self._create_rubies()

        pygame.display.set_caption('Rubies')

    def run_game(self) -> None: # Запуск игрового цикла
        while True:
            self._update_screen()
            self._check_events()

    def _check_events(self) -> None: # Функция обработки событий
        moving = None
        moving_id = None
        ruby = None
        old_x, old_y = None, None
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_q):
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                    mouse_pos = pygame.mouse.get_pos()
                    ruby, moving, moving_id = self._check_press_ruby(mouse_pos)
                    if ruby is not None:
                        old_x, old_y = ruby.rect.x, ruby.rect.y
                elif event.type == pygame.MOUSEMOTION and moving and moving_id == ruby.id:
                    x, y = event.rel
                    ruby.update_pos(x, y)
                    self._update_screen()
                elif event.type == pygame.MOUSEBUTTONUP and (event.button == 1 or event.button == 3):
                    moving = False
                    active = False
                    if ruby is not None:
                        self._check_replace(ruby, old_x, old_y)

    def _check_replace(self, ruby: Ruby, old_x: int, old_y: int) -> None: # Функция проверки наличия рубина?
        collisions = set(
            new_ruby for new_ruby in self.rubies_simple if ruby.rect.colliderect(new_ruby.rect))
        collisions = [i for i in collisions if i.id != ruby.id]
        if len(collisions) > 0:
            new_ruby = collisions[0]
            for i in range(-1, 2):
                stop = False
                for j in range(-1, 2):
                    if self.__is_valid_replace(ruby, i, j):
                        if self.rubies[ruby.id[0] + i][ruby.id[1] + j].id == new_ruby.id:
                            self._replace_rubies(ruby, new_ruby, old_x, old_y)
                            stop = True
                            break
                        ruby.rect.x, ruby.rect.y = old_x, old_y
                if stop:
                    break
        else:
            ruby.rect.x, ruby.rect.y = old_x, old_y

    def __is_valid_replace(self, ruby: Ruby, i: int, j: int) -> bool:
        if 0 <= ruby.id[0] + i < len(self.rubies) and 0 <= ruby.id[1] + j < len(
                self.rubies[0]) \
                and not (i == -1 and j == -1) and not (i == -1 and j == 1) and \
                not (i == 0 and j == 0) and not (i == 1 and j == -1) and not (
                i == 1 and j == 1):
            return True
        return False

    def _replace_rubies(self, ruby: Ruby, new_ruby: Ruby, old_x: int, old_y: int) -> None: # Функция замены рубинов
        ruby.id, new_ruby.id = new_ruby.id, ruby.id
        self.rubies[ruby.id[0]][ruby.id[1]], self.rubies[new_ruby.id[0]][
            new_ruby.id[1]] = \
            self.rubies[new_ruby.id[0]][new_ruby.id[1]], self.rubies[ruby.id[0]][
                ruby.id[1]]
        new_ruby.rect.x, new_ruby.rect.y, ruby.rect.x, ruby.rect.y = old_x, old_y, \
                                                                     new_ruby.rect.x, \
                                                                     new_ruby.rect.y
        for i in range(-1, 2, 2):
            for j in range(-1, 2):
                self._check_row(self.rubies[ruby.id[0] + i])
                self._check_row(self.rubies[new_ruby.id[0] + i])
                self._check_column(self.rubies)
        # self._check_row()
        # self._check_column()

    def _check_press_ruby(self, mouse_pos: tuple) -> tuple:
        for ruby_rows in self.rubies:
            for ruby in ruby_rows:
                if ruby.rect.collidepoint(mouse_pos):
                    moving = True
                    moving_id = ruby.id
                    return ruby, moving, moving_id
        return None, None, None

    def _check_row(self, row):
        memory = []
        for ruby_row in self.rubies:
            if len(memory) >= 3:
                self._change_rubies(memory)
            memory.clear()
            for ruby in ruby_row:
                if len(memory) == 0:
                    memory.append(ruby)
                    continue
                elif len(memory) >= 3:
                    if memory[0].color != ruby.color:
                        self._change_rubies(memory)
                        memory.clear()
                elif memory[0].color != ruby.color:
                    memory.clear()
                memory.append(ruby)

    def _check_column(self, column):
        memory = []
        for j in range(self.number_rubies_x):
            if len(memory) >= 3:
                self._change_rubies(memory)
            memory.clear()
            for i in range(self.number_rows):
                ruby = self.rubies[i][j]
                if len(memory) == 0:
                    memory.append(ruby)
                    continue
                elif len(memory) >= 3:
                    if memory[0].color != ruby.color:
                        self._change_rubies(memory)
                        memory.clear()
                elif memory[0].color != ruby.color:
                    memory.clear()
                memory.append(ruby)

    @staticmethod
    def _change_rubies(rubies):
        if len(rubies) > 0:
            for ruby in rubies:
                color = choice(COLORS)
                while color == ruby.color:
                    color = choice(COLORS)
                ruby.change_color(color)

    def _create_rubies(self): # Функция создания множества экземпляров класса Ruby
        ruby = Ruby(self, choice(COLORS))
        ruby_width, ruby_height = ruby.rect.size
        available_space_x = self.WIDTH - ruby_width * 2
        number_rubies_x = available_space_x // (ruby_width + ruby_width // 3)

        available_space_y = self.HEIGHT - (2 * ruby_height)
        number_rows = available_space_y // (ruby_width + ruby_width // 3)

        self.rubies = [[0] * number_rubies_x for _ in range(number_rows)]
        for row_number in range(number_rows):
            for ruby_number in range(number_rubies_x):
                self._create_ruby(ruby_number, row_number)
        return number_rows, number_rubies_x

    def _create_ruby(self, ruby_number, row_number): # Фунцкия создания одного экземпляра класса Ruby
        ruby = Ruby(self, choice(COLORS))
        ruby.id = (row_number, ruby_number)
        ruby_width, ruby_height = ruby.rect.size
        ruby.rect.x = ruby_width + (ruby_width + ruby_width // 2.4) * ruby_number
        ruby.rect.y = ruby_height + (ruby_width + ruby_width // 2.4) * row_number

        for rows in range(len(self.rubies)):
            stop = False
            for list_item in range(len(self.rubies[0])):
                self.rubies_simple.append(ruby)
                if self.rubies[rows][list_item] == 0:
                    self.rubies[rows][list_item] = ruby
                    stop = True
                    break
            if stop:
                break

    def _update_screen(self): # Функция создания кадров
        self.screen.fill('white')
        for ruby_row in self.rubies:
            for ruby in ruby_row:
                ruby.draw()
        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__': # Проверка на запуск как отдельного модуля
    rubies1 = Rubies()
    rubies1.run_game()
