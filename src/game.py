import pygame
import sys

from robot import Robot
from resources import Resources
from obstacles import Obstacles
from start_area import StartArea

from random import randint


class Game:
    def __init__(self, width: int, height: int, grid_size: int) -> None:
        self.width = width
        self.height = height
        self.grid_size: int = grid_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

        # Start Area
        self.start_area = StartArea(self.width, self.height)

        # Obtener las coordenadas de inicio generadas
        self.start_x = self.start_area.start_x
        self.start_y = self.start_area.start_y

        # Recursos
        self.resources: list[Resources] = [
            Resources(randint(0, width - 1),
                      randint(0, height - 1), width, height)
            for _ in range(20)
        ]
        # Obstáculos
        self.obstacles: list[Obstacles] = [
            Obstacles(randint(0, width - 1),
                      randint(0, height - 1), width, height)
            for _ in range(20)
        ]

        # Robots
        self.robots = [
            Robot(self.start_area.start_x,
                  self.start_area.start_y,
                  width, height),
            Robot(self.start_area.start_x,
                  self.start_area.start_y,
                  width, height),
            Robot(self.start_area.start_x,
                  self.start_area.start_y,
                  width, height),
            Robot(self.start_area.start_x,
                  self.start_area.start_y,
                  width, height)
        ]

        self.robot_colors: list[tuple] = [
            (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255))
        ]

        for robot in self.robots:
            robot.start_x = self.start_x
            robot.start_y = self.start_y

        # colors
        self.Grey = (100, 100, 100)

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(
            (width * grid_size, height * grid_size))
        pygame.display.set_caption("Grid")
        self.clock = pygame.time.Clock()

    def draw_grid(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.grid_size,
                                   y * self.grid_size,
                                   self.grid_size,
                                   self.grid_size)
                pygame.draw.rect(self.screen, self.Grey, rect, 1)

    def draw_resources(self) -> None:
        for resource in self.resources:
            resource.draw(self.screen, self.grid_size)

    def draw_obstacles(self) -> None:
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.grid_size)

    def draw_robot(self, robot: Robot, robot_color: tuple) -> None:
        rect = pygame.Rect(robot.x * self.grid_size,
                           robot.y * self.grid_size,
                           self.grid_size,
                           self.grid_size)
        pygame.draw.rect(self.screen, robot_color, rect)

    def move_robot(self, robot: Robot):
        if robot.is_grabbing:
            robot.return_to_start()
            if not robot.movements:
                robot.is_grabbing = False
        else:
            robot.move(self.robots, self.resources, self.obstacles)

    def run(self) -> None:
        running = True
        print(self.start_area.start_x, self.start_area.start_y)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            self.start_area.draw(self.screen, self.grid_size)
            self.draw_grid()
            self.draw_resources()
            self.draw_obstacles()
            for color, robot in enumerate(self.robots):
                self.draw_robot(robot, self.robot_colors[color - 1])
                self.move_robot(robot)

            pygame.display.flip()
            self.clock.tick(60)  # Cap the frame rate to 60 FPS

        pygame.quit()
        sys.exit()
