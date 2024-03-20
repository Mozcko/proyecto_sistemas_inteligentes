import pygame
import sys

from robot import Robot
from resources import Resources
from obstacles import Obstacles
from start_area import StartArea
from node import Cell

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
            Robot(self),
            # Robot(self.start_area.start_x,
            #       self.start_area.start_y,
            #       width, height),
            # Robot(self.start_area.start_x,
            #       self.start_area.start_y,
            #       width, height),
            # Robot(self.start_area.start_x,
            #       self.start_area.start_y,
            #       width, height)
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

    def move_robot(self, robot):
        # Check if the robot is carrying a resource
        if robot.is_grabbing:
            self.log("Robot is returning to the start area")
            # Find the closest cell in the start area
            start_cell = min(self.get_start_area_cells(), key=lambda cell: self.distance(robot, cell))

            # Move towards the start area
            reached_start_area = False
            while not reached_start_area:
                dx = start_cell.x - robot.x
                dy = start_cell.y - robot.y
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.update_closest_resource(robot)
                        robot.move_randomly()
                        if robot.x == start_cell.x and robot.y == start_cell.y:
                            reached_start_area = True
                            self.log("Robot has reached the start area")
                            break
                    else:
                        self.update_closest_resource(robot)
                        robot.move_randomly()
                        if robot.x == start_cell.x and robot.y == start_cell.y:
                            reached_start_area = True
                            self.log("Robot has reached the start area")
                            break
                else:
                    if dy > 0:
                        self.update_closest_resource(robot)
                        robot.move_randomly()
                        if robot.x == start_cell.x and robot.y == start_cell.y:
                            reached_start_area = True
                            self.log("Robot has reached the start area")
                            break
                    else:
                        self.update_closest_resource(robot)
                        robot.move_randomly()
                        if robot.x == start_cell.x and robot.y == start_cell.y:
                            reached_start_area = True
                            self.log("Robot has reached the start area")
                            break

            if not robot.movements:
                robot.is_grabbing = False
                self.log("Robot has dropped the resource")

        # Check if the robot knows the location of a resource
        else:
            self.log("Robot is moving towards a resource")
            closest_resource = min(self.resources, key=lambda resource: self.distance(robot, resource))

            # Move towards the closest resource
            if self.distance(robot, closest_resource) <= robot.view_distance:
                dx = closest_resource.x - robot.x
                dy = closest_resource.y - robot.y
                if abs(dx) > abs(dy):
                    if dx > 0:
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
                else:
                    if dy > 0:
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

            # If the robot can't see any resources, move randomly
            else:
                self.update_closest_resource(robot)
                robot.move_randomly()
                self.log("Robot is moving randomly")
    
    def distance(self, obj1, obj2):
        return abs(obj1.x - obj2.x) + abs(obj1.y - obj2.y)
    
    def update_closest_resource(self, robot):
        closest_resource = None
        closest_distance = float('inf')
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
            for color, robot in enumerate(self.robots):
                self.draw_robot(robot, self.robot_colors[color - 1])
                self.move_robot(robot)

            pygame.display.flip()
            self.clock.tick(20)  # Cap the frame rate to 60 FPS

        pygame.quit()
        sys.exit()
