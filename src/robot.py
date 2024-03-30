from typing import Union, List, Tuple, Optional
import random
from queue import PriorityQueue
from cell import Cell
from resources import Resources
from obstacles import Obstacles

class Robot:
    def __init__(self, game, x: int, y: int):
        self.game = game
        self.view_distance: int = 5
        self.grab_distance: int = 1
        self.materials: int = 0
        self.movements: List[Tuple[int, int]] = []
        self.explored_area = set()
        self.is_grabbing: bool = False
        self.closest_resource: Optional[Resources] = None
        self.last_resource: Optional[Resources] = None
        self.x: int = x
        self.y: int = y
        self.start_cell: Cell = Cell(self.x, self.y)
        self.current_path: Optional[List[Tuple[int, int]]] = None

    def decide_movement(self) -> None:
        # Buscar activamente el recurso más cercano dentro del campo de visión
        self.closest_resource = self.find_closest_resource()

        if self.last_resource is not None and self.last_resource.materials != 0:
            self.move_towards(self.last_resource)
            return
        elif self.closest_resource is not None and self.closest_resource.materials != 0:
            self.move_towards(self.closest_resource)
            return
        else:
            self.move_randomly()

    def find_closest_resource(self) -> Optional[Resources]:
        closest_resource = None
        closest_distance = float("inf")

        for resource in self.game.resources:
            distance = self.distance_to_resource(resource)
            if distance <= self.view_distance and distance < closest_distance:
                closest_resource = resource
                closest_distance = distance

        return closest_resource

    def move_randomly(self) -> None:
        direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        new_x, new_y = self.x + direction[0], self.y + direction[1]
        if self.is_valid_move(new_x, new_y):
            self._move(new_x, new_y)
            self._check_resource_interaction()  # Verificar interacción con recursos después de moverse


    def move_towards(self, target: Union[Cell, Resources]) -> None:
        if self.current_path:
            next_cell = self.current_path.pop(0)
            if self.is_valid_move(next_cell[0], next_cell[1]):
                self._move(next_cell[0], next_cell[1])
                self._check_resource_interaction()  # Verificar interacción con recursos después de moverse
        else:
            path = self.find_path_to(target)
            if path:
                next_cell = path.pop(0)
                if self.is_valid_move(next_cell[0], next_cell[1]):
                    self._move(next_cell[0], next_cell[1])
                    self.current_path = path
                    self._check_resource_interaction()  # Verificar interacción con recursos después de moverse
            else:
                self.move_randomly()

    def is_valid_move(self, x: int, y: int) -> bool:
        other_robots: List[Robot] = self.game.robots
        resources: List[Resources] = self.game.resources
        obstacles: List[Obstacles] = self.game.obstacles
        
        if not (0 <= x < self.game.width and 0 <= y < self.game.height):
            return False  # Movimiento fuera de los límites del tablero
        
        # Verificar colisión con otros robots
        collides_with_robots = any(robot.x == x and robot.y == y for robot in other_robots)
        
        # Verificar colisión con recursos
        collides_with_resources = any(resource.x == x and resource.y == y for resource in resources)
        if collides_with_resources:
            self.interact_with_resource(x, y)

        # Verificar colisión con obstáculos
        collides_with_obstacles = any(obstacle.x == x and obstacle.y == y for obstacle in obstacles)
        
        # Verificar si la posición ya ha sido explorada
        already_explored = (x, y) in self.explored_area
        
        # Si no hay colisiones y la posición no ha sido explorada, el movimiento es válido
        return not collides_with_robots and not collides_with_obstacles and not already_explored

    def _move(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self._check_resource_interaction()

    def interact_with_resource(self, x: int, y: int) -> None:
        for resource in self.game.resources:
            if resource.x == x and resource.y == y:
                if self.distance_to_resource(resource) <= self.grab_distance:
                    self.grab_resource(resource)
                    self.game.log("Robot has grabbed a resource")
                    self.closest_resource = None
                return

    def _check_resource_interaction(self) -> None:
        if self.closest_resource and self.distance_to_resource(self.closest_resource) <= self.grab_distance:
            # Verificar si el recurso está siendo agarrado por otro robot
            if not self.is_grabbing:
                self.grab_resource(self.closest_resource)
                self.game.log("Robot has grabbed a resource")
                self.closest_resource = None
        elif self.is_grabbing and self.distance_to_start_area() <= self.grab_distance:
            self.drop_resource()
            self.game.log("Robot has dropped a resource")
            
    def find_path_to(self, target: Union[Cell, Resources]) -> Optional[List[Tuple[int, int]]]:
        if isinstance(target, Cell):
            goal = (target.x, target.y)
        elif isinstance(target, Resources):
            goal = (target.x, target.y)
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
                new_cost = cost_so_far[current] + 1

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
            if self.is_valid_move(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors

    def distance_to_resource(self, resource: Resources) -> float:
        return self._calculate_distance(
            self.x, self.y, resource.x, resource.y
        )

    def distance_to_start_area(self) -> float:
        if not self.game.start_area:
            return float("inf")
        return self._calculate_distance(
            self.x, self.y, self.start_cell.x, self.start_cell.y
        )


    def _calculate_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def grab_resource(self, resource: Resources) -> None:
        if self.is_grabbing:
            return
        if self.distance_to_resource(resource) <= self.grab_distance:  # Corregir aquí
            self.materials += 1
            resource.materials -= 1
            self.is_grabbing = True
            self.last_resource = resource

    def drop_resource(self) -> None:
        if self.is_grabbing and self.distance_to_start_area() <= self.grab_distance:
            self.is_grabbing = False
            self.game.start_area.add_resource(self.materials)
            self.materials = 0
