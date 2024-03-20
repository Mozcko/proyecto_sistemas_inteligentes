import pygame

from random import randint


class StartArea:
    def __init__(self, grid_width, grid_height,
                 area_width=5, area_height=5) -> None:
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.area_width = area_width
        self.area_height = area_height
        self.start_x, self.start_y = self.generate_start_position()
        self.materials = 0

    def generate_start_position(self) -> tuple[int, int]:
        start_x = randint(0, self.grid_width - self.area_width)
        start_y = randint(0, self.grid_height - self.area_height)
        return start_x, start_y

    def increase_materials(self, amount: int) -> None:
        self.materials += amount

    def draw(self, screen, grid_size) -> None:
        for x in range(self.start_x, self.start_x + self.area_width):
            for y in range(self.start_y, self.start_y + self.area_height):
                rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
                pygame.draw.rect(screen, (128, 0, 128), rect)

    def add_resource(self, amount: int) -> None:
        self.materials += amount
