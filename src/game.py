# importes globales
import pygame
import sys

# importes locales
from random import randint
from typing import List, Tuple

# importes internos
from robot import Robot
from resources import Resources
from obstacles import Obstacles
from start_area import StartArea
from cell import Cell


class Game:
    def __init__(self, width: int, height: int, grid_size: int, ticks: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid_size: int = grid_size
        self.grid: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
        self.ticks: int = ticks

        self.number_of_robots: int = 4
        self.robots: List[Robot] = []

        # inicializa pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width * grid_size, height * grid_size))
        pygame.display.set_caption("Grid")
        self.clock = pygame.time.Clock()

        # inicializa los componentes del juego
        self.initialize_start_area()
        self.initialize_resources()
        self.initialize_obstacles()
        self.initialize_robots()

        # Colors
        self.GREY: Tuple[int, int, int] = (100, 100, 100)

        # Text
        self.font = pygame.font.Font(None, 24)  # Choose the font and size

    # funciones para inicializar los componentes del juego
    def initialize_start_area(self) -> None:
        self.start_area: StartArea = StartArea(self.width, self.height)
        self.start_x: int = self.start_area.start_x
        self.start_y: int = self.start_area.start_y

    def initialize_resources(self) -> None:
        self.resources: List[Resources] = [
            Resources(
                randint(0, self.width - 1),
                randint(0, self.height - 1),
                self.width,
                self.height,
            )
            for _ in range(20)
        ]

    def initialize_obstacles(self) -> None:
        self.obstacles: List[Obstacles] = [
            Obstacles(
                randint(0, self.width - 1),
                randint(0, self.height - 1),
                self.width,
                self.height,
            )
            for _ in range(20)
        ]

    def initialize_robots(self) -> None:
        for _ in range(self.number_of_robots):
            x: int = randint(
                self.start_x, self.start_x + self.start_area.area_width - 1
            )
            y: int = randint(
                self.start_y, self.start_y + self.start_area.area_height - 1
            )
            robot: Robot = Robot(self, x, y)
            self.robots.append(robot)

        self.robot_colors: List[Tuple[int, int, int]] = [
            (randint(0, 255), randint(0, 255), randint(0, 255)) for _ in self.robots
        ]

    # funciones para dibujar los componentes del juego
    def draw_grid(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * self.grid_size,
                    y * self.grid_size,
                    self.grid_size,
                    self.grid_size,
                )
                pygame.draw.rect(self.screen, self.GREY, rect, 1)

    def draw_resources(self) -> None:
        for resource in self.resources:
            resource.draw(self.screen, self.grid_size)

    def draw_obstacles(self) -> None:
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.grid_size)

    def draw_robot(self, robot: Robot, robot_color: Tuple[int, int, int]) -> None:
        rect = pygame.Rect(
            robot.x * self.grid_size,
            robot.y * self.grid_size,
            self.grid_size,
            self.grid_size,
        )
        pygame.draw.rect(self.screen, robot_color, rect)

    # dibuja el marcador
    def draw_text(self, text: str, position: Tuple[int, int]) -> None:
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def draw_info(self) -> None:
        start_area_materials_text = f"Start Area Materials: {self.start_area.materials}"
        self.draw_text(start_area_materials_text, (10, 10))

        robot_info_y = 30
        for i, robot in enumerate(self.robots):
            robot_materials_text = (
                f"Robot {i + 1} Grabbing: {robot.materials} materials"
            )
            self.draw_text(robot_materials_text, (10, robot_info_y))
            robot_info_y += 20

    # muestra información en consola
    def log(self, message: str) -> None:
        print(f"[{self.clock.get_rawtime()}] {message}")

    # calcula el movimiento del robot
    def move_robot(self, robot: Robot) -> None:
        if robot.is_grabbing:
            robot.move_towards(robot.start_cell)
        else:
            robot.decide_movement()

    # comprueba si el juego ha terminado
    def check_game_over(self) -> bool:
        return self.start_area.materials >= 25

    # ejecuta el juego
    def run(self) -> None:
        running: bool = True
        while running:

            # comprueba si no salen del juego
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # se dibujan todos los componentes del juego
            self.screen.fill((0, 0, 0))
            self.start_area.draw(self.screen, self.grid_size)
            self.draw_grid()
            self.draw_resources()
            self.draw_obstacles()
            self.draw_info()

            # actualización de los componentes del juego

            # actualización de los recursos
            for resource in self.resources:
                resource.update()
                if resource.materials == 0:
                    self.resources.remove(resource)

            # actualización de los robots
            for color, robot in enumerate(self.robots):
                if color < len(self.robot_colors):
                    self.draw_robot(robot, self.robot_colors[color])
                else:
                    self.draw_robot(robot, (0, 255, 0))

                if self.check_game_over():
                    robot.move_towards(robot.start_cell)
                else:
                    self.move_robot(robot)

            pygame.display.flip()
            self.clock.tick(self.ticks)

        pygame.quit()
        sys.exit()
