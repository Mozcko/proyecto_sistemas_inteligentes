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

        self.is_grabbing: bool = False
        self.materials: int = 0

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


        # Calculate the potential new position
        new_x: int = self.x + (left - right) * moving_x
        new_y: int = self.y + (down - up) * moving_y

        # Check if the new position is within the grid boundaries
        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
            # Check for collisions with other robots
            collides_with_robots = any(robot.x == new_x and robot.y == new_y for robot in other_robots)
            
            # Check for collisions with resources
            collides_with_resources = any(resource.x == new_x and resource.y == new_y for resource in resources)

            # Check for collisions with obstacles
            collides_with_obstacles = any(obstacle.x == new_x and obstacle.y == new_y for obstacle in obstacles)

            # If no collision with robots or resources, update the position
            if not collides_with_robots and not collides_with_obstacles:
                self.x = new_x
                self.y = new_y

            for resource in resources:
                if resource.x == new_x and resource.y == new_y:
                    grabbing_materials = randint(1, 2)
                    if resource.materials >= grabbing_materials and not self.is_grabbing:
                        self.materials += grabbing_materials
                        resource.materials -= self.materials
                        print(self.materials)
                        self.is_grabbing = self.materials >= 2
                        break
    
    def return_to_start(self, movements: list):
        pass

class Game:
    def __init__(self, width: int, height: int, grid_size: int):
        self.width = width
        self.height = height
        self.grid_size: int = grid_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

        # Resources
        self.resources: list[Obstacles] = [
            Resources(randint(0, width - 1), 
                      randint(0, height - 1), width, height) 
                      for _ in range(20)
                      ]
        # Obstacles
        self.obstacles: list[Obstacles] = [
            Obstacles(randint(0, width - 1), 
                      randint(0, height - 1), width, height) 
                      for _ in range(20)
                      ]

        # Robots
        self.robots = [
            Robot(randint(0, self.width - 1), randint(0, self.height - 1), self.width, self.height),
            Robot(randint(0, self.width - 1), randint(0, self.height - 1), self.width, self.height),
            Robot(randint(0, self.width - 1), randint(0, self.height - 1), self.width, self.height),
            Robot(randint(0, self.width - 1), randint(0, self.height - 1), self.width, self.height)
        ]


        # colors
        self.White = (255, 255, 255)
        

        # Initialize Pygame
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
        robot.move(self.robots, self.resources, self.obstacles)

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
            for robot in self.robots:
                self.draw_robot(robot)
                self.move_robot(robot)

            
            pygame.display.flip()
            self.clock.tick(10)  # Cap the frame rate to 60 FPS

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game(75, 40, 20)  # 75x40 grid with each cell being 20x20 pixels
    game.run()