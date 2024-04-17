# importes globales
import pygame

# importes locales
from random import randint


class StartArea:
    def __init__(
        self,
        grid_width: int,
        grid_height: int,
        area_width: int = 5,
        area_height: int = 5,
    ) -> None:
        self.grid_width: int = grid_width
        self.grid_height: int = grid_height
        self.area_width: int = area_width
        self.area_height: int = area_height
        self.start_x: int
        self.start_y: int
        self.generate_start_position()
        self.x: int = self.start_x
        self.y: int = self.start_y
        self.materials: int = 0

    def generate_start_position(self) -> None:
        self.start_x: int = randint(0, self.grid_width - self.area_width)
        self.start_y: int = randint(0, self.grid_height - self.area_height)

    def increase_materials(self) -> None:
        self.materials += 1

    def draw(self, screen: pygame.Surface, grid_size: int) -> None:
        for x in range(self.start_x, self.start_x + self.area_width):
            for y in range(self.start_y, self.start_y + self.area_height):
                rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
                pygame.draw.rect(screen, (128, 0, 128), rect)
