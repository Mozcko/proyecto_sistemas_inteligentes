import math

from random import randint
from obstacles import Obstacles
from resources import Resources
from start_area import StartArea


class Robot:
    def __init__(self, x: int, y: int, grid_width: int,
                 grid_height: int) -> None:
        self.start_x: int = x
        self.start_y: int = y
        self.x: int = x
        self.y: int = y
        self.grid_width: int = grid_width
        self.grid_height: int = grid_height

        self.is_grabbing: bool = False
        self.materials: int = 0
        self.movements: list = []
        self.explored_area: set = set()

    def move(self, other_robots: list, resources: list[Resources],
             obstacles: list[Obstacles]) -> None:
        left = randint(0, 1)
        right = randint(0, 1)
        up = randint(0, 1)
        down = randint(0, 1)

        moving_x = randint(0, 1)
        if moving_x == 0:
            moving_y = 1
        else:
            moving_y = 0

        # Calculate the potential new position
        new_x = self.x + (left - right) * moving_x
        new_y = self.y + (down - up) * moving_y

        # Check if the new position is within the grid boundaries
        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
            # Check for collisions with other robots
            collides_with_robots = any(robot.x == new_x and robot.y == new_y for robot in other_robots)

            # Check for collisions with resources
            collides_with_resources = any(resource.x == new_x and resource.y == new_y for resource in resources)

            # Check for collisions with obstacles
            collides_with_obstacles = any(obstacle.x == new_x and obstacle.y == new_y for obstacle in obstacles)

            # Check if the new position is already explored
            already_explored = (new_x, new_y) in self.explored_area

            for resource in resources:
                if resource.x == new_x and resource.y == new_y:
                    self.grab_resource(resource)

            if not collides_with_robots and not collides_with_obstacles and not collides_with_resources:
                if not already_explored:
                    self.x = new_x
                    self.y = new_y
                    movement = (self.x, self.y)
                    self.movements.append(movement)
                    self.explored_area.add(movement)
                elif randint(1,2) == 2:
                    self.x = new_x
                    self.y = new_y
                    movement = (self.x, self.y)
                    self.movements.append(movement)


    def return_to_start(self) -> None:
        if self.is_grabbing and self.movements:
            # Pop the last movement
            x, y = self.movements.pop()
            # Revert the movement
            self.x = x
            self.y = y

            # Check if the robot has returned to the start point
            if self.x == self.start_x and self.y == self.start_y:
                # Reset robot's state
                self.materials = 0
                self.change_grabbing_status()
                print("Robot returned to start point.")
                return

    def grab_resource(self, resource) -> None:
        print("is grabbing")
        grabbing_materials = randint(1, 2)
        if resource.materials >= grabbing_materials and not self.is_grabbing:
            self.materials += grabbing_materials
            resource.materials -= grabbing_materials
            self.change_grabbing_status()

    def change_grabbing_status(self) -> None:
        if self.is_grabbing:
            self.is_grabbing = False
        else:
            self.is_grabbing = True

    def make_move(self, new_x, new_y) -> None:
        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
            movement = (self.x - new_x, self.y - new_y)  # Guardar el movimiento
            self.movements.append(movement)
            self.x = new_x
            self.y = new_y

    def is_touching_start_area(self, threshold: float, start_area: StartArea) -> bool:
        distance = math.sqrt((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2)
        return distance <= threshold
