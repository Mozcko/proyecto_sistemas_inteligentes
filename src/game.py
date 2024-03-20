import pygame
import sys

from robot import Robot
from resources import Resources
from obstacles import Obstacles
from start_area import StartArea
from cell import Cell

from random import randint


class Game:
    def __init__(self, width: int, height: int, grid_size: int) -> None:
        self.width = width
        self.height = height
        self.grid_size: int = grid_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

        self.number_of_robots = 4
        self.robots = []

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width * grid_size, height * grid_size))
        pygame.display.set_caption("Grid")
        self.clock = pygame.time.Clock()

        # Initialize game components
        self.initialize_start_area()
        self.initialize_resources()
        self.initialize_obstacles()
        self.initialize_robots()

        # Colors
        self.Grey = (100, 100, 100)

        # Text
        self.font = pygame.font.Font(None, 24)  # Choose the font and size

    def initialize_start_area(self):
        self.start_area = StartArea(self.width, self.height)
        self.start_x = self.start_area.start_x
        self.start_y = self.start_area.start_y

    def initialize_resources(self):
        self.resources = [
            Resources(
                randint(0, self.width - 1),
                randint(0, self.height - 1),
                self.width,
                self.height,
            )
            for _ in range(20)
        ]

    def initialize_obstacles(self):
        self.obstacles = [
            Obstacles(
                randint(0, self.width - 1),
                randint(0, self.height - 1),
                self.width,
                self.height,
            )
            for _ in range(20)
        ]

    def initialize_robots(self):
        start_x, start_y = self.start_area.start_x, self.start_area.start_y
        area_width, area_height = (
            self.start_area.area_width,
            self.start_area.area_height,
        )

        for robot in range(self.number_of_robots):
            # Place robots randomly within the start area
            x = randint(start_x, start_x + area_width - 1)
            y = randint(start_y, start_y + area_height - 1)
            robot: Robot = Robot(self, x, y)
            self.robots.append(robot)

        self.robot_colors = [
            (randint(0, 255), randint(0, 255), randint(0, 255)) for _ in self.robots
        ]

    def draw_grid(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * self.grid_size,
                    y * self.grid_size,
                    self.grid_size,
                    self.grid_size,
                )
                pygame.draw.rect(self.screen, self.Grey, rect, 1)

    def draw_resources(self) -> None:
        for resource in self.resources:
            resource.draw(self.screen, self.grid_size)

    def draw_obstacles(self) -> None:
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.grid_size)

    def draw_robot(self, robot: Robot, robot_color: tuple) -> None:
        rect = pygame.Rect(
            robot.x * self.grid_size,
            robot.y * self.grid_size,
            self.grid_size,
            self.grid_size,
        )
        pygame.draw.rect(self.screen, robot_color, rect)

    def move_robot(self, robot):
        if robot.is_grabbing:
            self.return_to_start_area(robot)
        else:
            self.move_towards_resource(robot)

    def return_to_start_area(self, robot):
        start_cell = min(
            self.get_start_area_cells(), key=lambda cell: self.distance(robot, cell)
        )
        dx = start_cell.x - robot.x
        dy = start_cell.y - robot.y
        if abs(dx) > abs(dy):
            self.update_closest_resource(robot)
            robot.move_randomly()
        else:
            self.update_closest_resource(robot)
            robot.move_randomly()

        if robot.x == start_cell.x and robot.y == start_cell.y:
            robot.is_grabbing = False
            self.log("Robot has returned to the start area")
            self.log("Robot has dropped the resource")

    def move_towards_resource(self, robot):
        closest_resource = min(
            self.resources, key=lambda resource: self.distance(robot, resource)
        )
        dx = closest_resource.x - robot.x
        dy = closest_resource.y - robot.y
        if abs(dx) > abs(dy):
            self.update_closest_resource(robot)
            robot.move_randomly()
            if robot.x == closest_resource.x and robot.y == closest_resource.y:
                robot.grab_resource(closest_resource)
                self.log("Robot has grabbed a resource")
        else:
            self.update_closest_resource(robot)
            robot.move_randomly()
            if robot.x == closest_resource.x and robot.y == closest_resource.y:
                robot.grab_resource(closest_resource)
                self.log("Robot has grabbed a resource")

    def distance(self, obj1, obj2):
        return abs(obj1.x - obj2.x) + abs(obj1.y - obj2.y)

    def update_closest_resource(self, robot):
        closest_resource = None
        closest_distance = float("inf")
        for resource in self.resources:
            distance = abs(robot.x - resource.x) + abs(robot.y - resource.y)
            if distance < closest_distance:
                closest_resource = resource
                closest_distance = distance
        robot.closest_resource = closest_resource

    def is_obstacle(self, position):
        return position in self.obstacles

    def get_start_area_cells(self):
        start_area_cells = []
        start_x, start_y = self.start_area.start_x, self.start_area.start_y
        width, height = self.start_area.area_width, self.start_area.area_height

        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                cell_x, cell_y = x // self.grid_size, y // self.grid_size
                start_area_cells.append((cell_x, cell_y))

        # Convert the tuples to Cell objects
        start_area_cells = [Cell(x, y) for x, y in start_area_cells]

        return start_area_cells

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))  # White color
        self.screen.blit(text_surface, position)

    def draw_info(self):
        start_area_materials_text = f"Start Area Materials: {self.start_area.materials}"
        self.draw_text(start_area_materials_text, (10, 10))

        # Draw information about each robot
        robot_info_y = 30
        for i, robot in enumerate(self.robots):
            robot_materials_text = f"Robot {i + 1} Materials: {robot.materials}"
            self.draw_text(robot_materials_text, (10, robot_info_y))
            robot_info_y += 20

            if robot.is_grabbing:
                grabbing_text = f"Robot {i + 1} is Grabbing"
                self.draw_text(grabbing_text, (10, robot_info_y))
                robot_info_y += 20

    def log(self, message):
        print(f"[{self.clock.get_time()}] {message}")

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
            self.draw_info()  # Draw the information
            for color, robot in enumerate(self.robots):
                # Draw each robot and move them
                if color < len(self.robot_colors):
                    self.draw_robot(robot, self.robot_colors[color])
                else:
                    self.draw_robot(robot, (255, 255, 255))  # White color
                self.move_robot(robot)

            pygame.display.flip()
            self.clock.tick(20)  # Cap the frame rate to 20 FPS

        pygame.quit()
        sys.exit()
