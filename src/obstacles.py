import pygame


class Obstacles:
    def __init__(self, x, y, grid_width, grid_height) -> None:
        self.x = x
        self.y = y
        self.grid_width = grid_width
        self.grid_height = grid_height

    def draw(self, screen, grid_size) -> None:
        rect = pygame.Rect(self.x * grid_size,
                           self.y * grid_size,
                           grid_size, grid_size)
        pygame.draw.rect(screen, (255, 0, 0), rect)
