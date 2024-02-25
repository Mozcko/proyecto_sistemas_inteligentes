import pygame
import sys
from random import randint

class Obstacles:
    def __init__(self, x, y, grid_width, grid_height):
        self.x = x
        self.y = y
        self.grid_width = grid_width
        self.grid_height = grid_height

    def draw(self, screen, grid_size):
        rect = pygame.Rect(self.x * grid_size, self.y * grid_size, grid_size, grid_size)
        pygame.draw.rect(screen, (255, 0, 0), rect)


class Resources(Obstacles):
    def __init__(self, x, y, grid_width, grid_height):
        super().__init__(x, y, grid_width, grid_height)
        self.materials = randint(1, 6)

    def generate(self):
        self.x = randint(0, self.grid_width - 1)
        self.y = randint(0, self.grid_height - 1)
        self.materials = randint(1, 6)

    def update(self):
        if self.materials == 0:
            pass

    def draw(self, screen, grid_size):
        rect = pygame.Rect(self.x * grid_size, self.y * grid_size, grid_size, grid_size)
        pygame.draw.rect(screen, (0, 0, 255), rect)


class Robot:
    def __init__(self, x, y, grid_width, grid_height):
        self.x = x
        self.y = y
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.start_x = 0  # Se inicializará más adelante
        self.start_y = 0  # Se inicializará más adelante

        self.is_grabbing: bool = False
        self.materials: int = 0
        self.movements = []  # Lista para almacenar los movimientos

    def move(self, other_robots, resources, obstacles):
        left: bool = randint(0, 1)
        right: bool = randint(0, 1)
        up: bool = randint(0, 1)
        down: bool = randint(0, 1)

        moving_x = randint(0, 1)
        if moving_x == 0:
            moving_y = 1
        else:
            moving_y = 0

        new_x: int = self.x + (left - right) * moving_x
        new_y: int = self.y + (down - up) * moving_y

        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
            collides_with_robots = any(robot.x == new_x and robot.y == new_y for robot in other_robots)
            collides_with_resources = any(resource.x == new_x and resource.y == new_y for resource in resources)
            collides_with_obstacles = any(obstacle.x == new_x and obstacle.y == new_y for obstacle in obstacles)

            if not collides_with_robots and not collides_with_obstacles:
                self.x = new_x
                self.y = new_y

            for resource in resources:
                if resource.x == new_x and resource.y == new_y:
                    grabbing_materials = randint(1, 2)
                    if resource.materials >= grabbing_materials and not self.is_grabbing:
                        self.materials += grabbing_materials
                        resource.materials -= self.materials
                        self.is_grabbing = self.materials >= 2
                        break
    
    def return_to_start(self):
        if self.is_grabbing:
            movements_back = self.movements[::-1]  
            for movement in movements_back:
                self.x -= movement[0]  
                self.y -= movement[1]  
                self.movements.pop()  
                if self.x == self.start_x and self.y == self.start_y:
                    self.materials = 0
                    self.is_grabbing = False
                    break

class Game:
    def __init__(self, width: int, height: int, grid_size: int):
        self.width = width
        self.height = height
        self.grid_size: int = grid_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

        self.White = (255, 255, 255)
        
        pygame.init()
        self.screen = pygame.display.set_mode((width * grid_size, height * grid_size))
        pygame.display.set_caption("Grid")
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def draw_resources(self):
        for resource in self.resources:
            resource.draw(self.screen, self.grid_size)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.grid_size)

    def draw_robot(self, robot: Robot):
        rect = pygame.Rect(robot.x * self.grid_size, robot.y * self.grid_size, self.grid_size, self.grid_size)
        pygame.draw.rect(self.screen, (0, 255, 0), rect)

    def move_robot(self, robot: Robot):
        # Se guarda el movimiento antes de realizarlo
        movement = (robot.x - robot.start_x, robot.y - robot.start_y)
        robot.movements.append(movement)
        robot.move(self.robots, self.resources, self.obstacles)

    def generate_start_area(self):
        start_x = randint(0, self.width - 6)  # Genera un área de 5x5
        start_y = randint(0, self.height - 6)
        for x in range(start_x, start_x + 5):
            for y in range(start_y, start_y + 5):
                self.grid[y][x] = 1  # Marca la ubicación del área de inicio
        return start_x, start_y

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_resources()
            self.draw_obstacles()
            
            # Generar área de inicio si aún no se ha generado
            if not hasattr(self, 'robots_initialized'):
                self.robots_initialized = True
                self.start_x, self.start_y = self.generate_start_area()
                for robot in self.robots:
                    robot.start_x = self.start_x
                    robot.start_y = self.start_y

            for robot in self.robots:
                self.draw_robot(robot)
                self.move_robot(robot)
                robot.return_to_start()

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game(75, 40, 20)  
