# importes externos
import random

from cell import Cell


class Robot:
    def __init__(self, game, x, y):
        self.game = game
        self.view_distance = 5
        self.materials = 0
        self.movements = []
        self.is_grabbing = False
        self.closest_resource = None
        self.x = x
        self.y = y
        self.start_cell = Cell(self.x, self.y)

    def move_randomly(self):
        direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        new_x, new_y = self.x + direction[0], self.y + direction[1]
        if self._is_valid_move(new_x, new_y):
            self._move(new_x, new_y)

    def move_towards(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        if abs(dx) > abs(dy):
            self._move(self.x + 1 if dx > 0 else self.x - 1, self.y)
        else:
            self._move(self.x, self.y + 1 if dy > 0 else self.y - 1)

    def _is_valid_move(self, x, y):
        return (
            0 <= x < self.game.width
            and 0 <= y < self.game.height
            and not self.game.is_obstacle((x, y))
        )

    def _move(self, x, y):
        self.x, self.y = x, y
        self._check_resource_interaction()

    def _check_resource_interaction(self):
        if self.closest_resource and self.distance_to_resource() <= self.view_distance:
            self.grab_resource(self.closest_resource)
            self.game.log("Robot has grabbed a resource")
            self.closest_resource = None
        elif self.is_grabbing and self.distance_to_start_area() <= self.view_distance:
            self.drop_resource()
            self.game.log("Robot has dropped a resource")

    def distance_to_resource(self):
        if not self.closest_resource:
            return float("inf")
        return self._calculate_distance(
            self.x, self.y, self.closest_resource.x, self.closest_resource.y
        )

    def distance_to_start_area(self):
        if not self.game.start_area:
            return float("inf")
        return self._calculate_distance(
            self.x, self.y, self.start_cell.x, self.start_cell.y
        )

    def _calculate_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def grab_resource(self, resource):
        if self.is_grabbing:
            return
        if self.distance_to_resource() <= 1:
            self.materials += resource.materials
            self.is_grabbing = True
            resource.is_grabbed = True

    def drop_resource(self):
        if self.is_grabbing and self.distance_to_start_area() <= 1:
            self.is_grabbing = False
            self.game.start_area.add_resource(self.materials)
            self.materials = 0
