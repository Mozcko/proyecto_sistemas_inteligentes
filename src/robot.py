from typing import Union, List, Tuple, Optional
import random
from queue import PriorityQueue
from cell import Cell
from resources import Resources

class Robot:
    def __init__(self, game, x: int, y: int):
        self.game = game
        self.view_distance: int = 5
        self.materials: int = 0
        self.movements: List[Tuple[int, int]] = []
        self.is_grabbing: bool = False
        self.closest_resource: Optional[Resources] = None
        self.last_resource: Optional[Resources] = None
        self.x: int = x
        self.y: int = y
        self.start_cell: Cell = Cell(self.x, self.y)
        self.current_path: Optional[List[Tuple[int, int]]] = None

    def move_randomly(self) -> None:
        direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        new_x, new_y = self.x + direction[0], self.y + direction[1]
        if self._is_valid_move(new_x, new_y):
            self._move(new_x, new_y)

    def move_towards(self, target: Union[Cell, Resources]) -> None:
        if self.current_path:
            next_cell = self.current_path.pop(0)
            self._move(next_cell[0], next_cell[1])
        else:
            path = self.find_path_to(target)
            if path:
                self.current_path = path
                self.move_towards(target)
            else:
                if isinstance(target, Resources):
                    self.move_randomly()
                elif isinstance(target, Cell):
                    self.move_randomly()  # You might want to change this behavior

    def _is_valid_move(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.game.width
            and 0 <= y < self.game.height
            and not self.game.is_obstacle((x, y))
        )

    def _move(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self._check_resource_interaction()

    def _check_resource_interaction(self) -> None:
        if self.closest_resource and self.distance_to_resource() <= self.view_distance:
            self.grab_resource(self.closest_resource)
            self.game.log("Robot has grabbed a resource")
            self.closest_resource = None
        elif self.is_grabbing and self.distance_to_start_area() <= self.view_distance:
            self.drop_resource()
            self.game.log("Robot has dropped a resource")

    def find_path_to(self, target: Union[Cell, Resources]) -> Optional[List[Tuple[int, int]]]:
        if isinstance(target, Cell):
            goal = (target.x, target.y)
        elif isinstance(target, Resources):
            goal = (target.x, target.y)  # Assuming Resources has x and y attributes
        else:
            raise ValueError("Invalid target type")

        start = (self.x, self.y)
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next_cell in self._get_neighbors(current[0], current[1]):
                new_cost = cost_so_far[current] + 1  # Assuming each step costs 1

                if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                    cost_so_far[next_cell] = new_cost
                    priority = new_cost + self._calculate_distance(goal[0], goal[1], next_cell[0], next_cell[1])
                    frontier.put(next_cell, priority)
                    came_from[next_cell] = current

        if goal in came_from:
            path = []
            current = goal
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        else:
            return None

    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if self._is_valid_move(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors

    def distance_to_resource(self) -> float:
        if not self.closest_resource:
            return float("inf")
        return self._calculate_distance(
            self.x, self.y, self.closest_resource.x, self.closest_resource.y
        )

    def distance_to_start_area(self) -> float:
        if not self.game.start_area:
            return float("inf")
        return self._calculate_distance(
            self.x, self.y, self.start_cell.x, self.start_cell.y
        )

    def _calculate_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return abs(x1 - x2) + abs(y1 - y2)

    def grab_resource(self, resource: Resources) -> None:
        if self.is_grabbing:
            return
        if self.distance_to_resource() <= 1:
            self.materials += resource.materials
            self.is_grabbing = True
            resource.is_grabbed = True

    def drop_resource(self) -> None:
        if self.is_grabbing and self.distance_to_start_area() <= 1:
            self.is_grabbing = False
            self.game.start_area.add_resource(self.materials)
            self.materials = 0
