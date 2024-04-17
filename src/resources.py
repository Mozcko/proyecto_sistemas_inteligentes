# importes globales
import pygame

# importes locales
from random import randint

# importes internos
from obstacles import Obstacles


class Resources(Obstacles):
    def __init__(self, x: int, y: int, grid_width: int, grid_height: int) -> None:
        super().__init__(x, y, grid_width, grid_height)
        self.materials: int = randint(1, 6)

    def generate(self) -> None:
        self.x = randint(0, self.grid_width - 1)
        self.y = randint(0, self.grid_height - 1)
        self.materials = randint(1, 6)

    def update(self) -> None:
        if self.materials == 0:
            self.x = -1
            self.y = -1

    def draw(self, screen: pygame.Surface, grid_size: int) -> None:
        rect = pygame.Rect(self.x * grid_size, self.y * grid_size, grid_size, grid_size)
        pygame.draw.rect(screen, (0, 0, 255), rect)
