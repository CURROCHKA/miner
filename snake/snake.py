import pygame


class Snake:
    def __init__(self, coord: tuple, size: tuple, color: str = 'green'):
        self.x, self.y = coord
        self.size = size
        self.color = color
        self.snake_list = [(self.x, self.y)]
        self.moving_x, self.moving_y = 0, 0
        self.speed = 1
        self.len = 1

    def __len__(self):
        return len(self.snake_list)

    def update(self, screen_rect: pygame.Rect):
        self.x += self.size[0] * self.moving_x * self.speed
        self.y += self.size[1] * self.moving_y * self.speed

        if self.x >= screen_rect.right:
            self.x = 0
        if self.x < 0:
            self.x = int(screen_rect.right - screen_rect.right % self.size[0])
        if self.y < 0:
            self.y = int(screen_rect.bottom - screen_rect.bottom % self.size[1])
        if self.y >= screen_rect.bottom:
            self.y = 0

        # ОБНОВЛЕНИЕ snake_list путем добавления ячейки змеи в список и удаление, если фактическая длина змеи меньше
        if self.speed == 1:
            self.snake_list.append((self.x, self.y))
        if len(self.snake_list) > self.len:
            del self.snake_list[0]
    
    def draw(self, surface: pygame.Surface):
        for cell in self.snake_list:
            pygame.draw.rect(surface, self.color, [cell[0], cell[1], self.size[0], self.size[1]])
