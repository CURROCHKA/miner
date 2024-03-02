import pygame


class Snake:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.size = (25, 25)
        self.x = int(self.screen_rect.centerx - self.screen_rect.centerx % self.size[0])
        self.y = int(self.screen_rect.centery - self.screen_rect.centery % self.size[1])
        self.snake_list = [(self.x, self.y)]
        self.color = 'green'
        self.moving_x, self.moving_y = 0, 0
        self.speed = 1
        self.len_of_snake = 1

    def __len__(self):
        return len(self.snake_list)

    def update(self):
        self.x += self.size[0] * self.moving_x * self.speed
        self.y += self.size[1] * self.moving_y * self.speed

        if self.x >= self.screen_rect.right:
            self.x = 0
        if self.x < 0:
            self.x = int(self.screen_rect.right - self.screen_rect.right % self.size[0])
        if self.y < 0:
            self.y = int(self.screen_rect.bottom - self.screen_rect.bottom % self.size[1])
        if self.y >= self.screen_rect.bottom:
            self.y = 0

        # ОБНОВЛЕНИЕ snake_list путем добавления ячейки змеи в список и удаление, если фактическая длина змеи меньше
        if self.speed == 1:
            self.snake_list.append((self.x, self.y))
        if len(self.snake_list) > self.len_of_snake:
            del self.snake_list[0]
    
    def draw(self, surface: pygame.Surface):
        for cell in self.snake_list:
            pygame.draw.rect(surface, self.color, [cell[0], cell[1], self.size[0], self.size[1]])
