from typing import Union, List, Tuple, Optional
import random
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
            distance = self.distance_to(resource)
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
        target_x, target_y = target.x, target.y
        if self.distance_to(target) > 0:
            direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            new_x, new_y = self.x + direction[0], self.y + direction[1]
            closer_to_target: bool = False
            while not closer_to_target and self.is_valid_move(new_x, new_y):
                direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
                new_x, new_y = self.x + direction[0], self.y + direction[1]
                closer_to_target = abs(new_x - target_x) + abs(new_y - target_y) <= self.distance_to(target)
            else:
                self._move(new_x, new_y)

    def is_valid_move(self, x: int, y: int) -> bool:
        # other_robots: List[Robot] = self.game.robots
        resources: List[Resources] = self.game.resources
        obstacles: List[Obstacles] = self.game.obstacles
        
        if not (0 <= x < self.game.width and 0 <= y < self.game.height):
            return False  # Movimiento fuera de los límites del tablero
        
        # Verificar colisión con otros robots
        # collides_with_robots = any(robot.x == x and robot.y == y for robot in other_robots)
        
        # Verificar colisión con recursos
        collides_with_resources = any(resource.x == x and resource.y == y for resource in resources)
        if collides_with_resources:
            self.interact_with_resource(x, y)

        # Verificar colisión con obstáculos
        collides_with_obstacles = any(obstacle.x == x and obstacle.y == y for obstacle in obstacles)
        
        # Verificar si la posición ya ha sido explorada
        already_explored = (x, y) in self.explored_area
        
        # Si no hay colisiones y la posición no ha sido explorada, el movimiento es válido
        return not collides_with_obstacles and not already_explored and not collides_with_resources

    def _move(self, x: int, y: int) -> None:
        self.movements.append((x, y))
        self.x, self.y = x, y
        self._check_resource_interaction()

    def interact_with_resource(self, x: int, y: int) -> None:
        for resource in self.game.resources:
            if resource.x == x and resource.y == y:
                if self.distance_to(resource) <= self.grab_distance:
                    self.grab_resource(resource)
                    self.game.log("Robot has grabbed a resource")
                    self.is_grabbing = True
                    self.closest_resource = None
                return

    def _check_resource_interaction(self) -> None:
        if self.closest_resource and self.distance_to(self.closest_resource) <= self.grab_distance:
            # Verificar si el recurso está siendo agarrado por otro robot
            if not self.is_grabbing:
                self.grab_resource(self.closest_resource)
                self.game.log("Robot has grabbed a resource")
                self.closest_resource = None
             
        elif self.is_grabbing and (self.distance_to(self.start_cell) == self.grab_distance):
            self.drop_resource()
            self.game.log("Robot has dropped a resource")

    def ask_for_help(self, resource: Resources):
        if resource.materials > 0:
            for robot in self.game.robots:
                if robot.last_resource and not robot == self:
                    robot.last_resource = resource

    def distance_to(self, target: Union[Resources, Cell]):
        return abs(self.x - target.x) + abs(self.y - target.y)

    def grab_resource(self, resource: Resources) -> None:
        if self.is_grabbing:
            return
        if self.distance_to(resource) <= self.grab_distance:  # Corregir aquí
            self.materials += 1
            resource.materials -= 1
            self.is_grabbing = True
            self.last_resource = resource
            self.ask_for_help(resource)

    def drop_resource(self) -> None:
        if self.is_grabbing and self.distance_to(self.start_cell) == self.grab_distance:
            self.is_grabbing = False
            self.game.start_area.increase_materials()
            self.materials = 0
