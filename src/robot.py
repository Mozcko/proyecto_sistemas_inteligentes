# importes externos
import random
from math import sqrt

# importes internos
from obstacles import Obstacles
from resources import Resources
from start_area import StartArea
from node import Node


class Robot:
    def __init__(self, game):
        self.game = game
        self.start_cell = random.choice(self.game.get_start_area_cells()) 
        print(self.start_cell.x)
        self.x = self.start_cell.x
        self.y = self.start_cell.y
        self.view_distance = 5
        self.materials = 0
        self.movements = []
        self.is_grabbing = False
        self.closest_resource = None

    def move_randomly(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        direction = random.choice(directions)

        # Check if the move is valid (i.e., not into an obstacle or off the grid)
        new_x, new_y = self.x + direction[0], self.y + direction[1]
        if 0 <= new_x < self.game.width and 0 <= new_y < self.game.height and not self.game.is_obstacle((new_x, new_y)):
            self.x, self.y = new_x, new_y
            self.movements.append(direction)

            # If the robot is moving towards a resource, check if it has reached the resource
            if self.closest_resource and self.distance_to_resource() <= self.view_distance:
                self.grab_resource(self.closest_resource)
                self.game.log("Robot has grabbed a resource")
                self.closest_resource = None

            # If the robot is carrying a resource, check if it has reached the start area
            elif self.is_grabbing and self.distance_to_start_area() <= self.view_distance:
                self.drop_resource()
                self.game.log("Robot has dropped a resource")

    def distance_to_resource(self):
        if not self.closest_resource:
            return float('inf')
        return abs(self.x - self.closest_resource.x) + abs(self.y - self.closest_resource.y)
    
    def distance_to_start_area(self):
        if not self.game.start_area:
            return float('inf')
        start_cell = min(self.game.get_start_area_cells(), key=lambda cell: self.game.distance(cell))
        return abs(self.x - start_cell.x) + abs(self.y - start_cell.y)

    def move_towards(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        if abs(dx) > abs(dy):
            if dx > 0:
                self.move_randomly(1, 0)
            else:
                self.move_randomly(-1, 0)
        else:
            if dy > 0:
                self.move_randomly(0, 1)
            else:
                self.move_randomly(0, -1)

    def grab_resource(self, resource):
        if self.is_grabbing:
            return

        if self.distance_to_resource() <= 1:
            self.materials += resource.materials
            self.is_grabbing = True
            resource.is_grabbed = True

    def return_to_start(self, start_area):
        if not self.is_grabbing:
            return

        if self.distance(self, start_area) <= 1:
            self.is_grabbing = False
            start_area.add_resource(self.materials)
            self.materials = 0