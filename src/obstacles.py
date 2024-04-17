import pygame


class Obstacles:
    def __init__(self, x: int, y: int, grid_width: int, grid_height: int) -> None:
        self.x: int = x
        self.y: int = y
        self.grid_width: int = grid_width
        self.grid_height: int = grid_height

    def draw(self, screen: pygame.Surface, grid_size: int) -> None:
        rect = pygame.Rect(self.x * grid_size, self.y * grid_size, grid_size, grid_size)
        pygame.draw.rect(screen, (255, 0, 0), rect)
