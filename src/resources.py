import pygame
from random import randint

from obstacles import Obstacles


class Resources(Obstacles):
    def __init__(self, x, y, grid_width, grid_height) -> None:
        super().__init__(x, y, grid_width, grid_height)
        self.materials = randint(1, 6)

    def generate(self) -> None:
        self.x = randint(0, self.grid_width - 1)
        self.y = randint(0, self.grid_height - 1)
        self.materials = randint(1, 6)

    def update(self) -> None:
        if self.materials == 0:
            self.x = -1
            self.y = -1

    def draw(self, screen, grid_size) -> None:
        rect = pygame.Rect(self.x * grid_size,
                           self.y * grid_size,
                           grid_size, grid_size)
        pygame.draw.rect(screen, (0, 0, 255), rect)
