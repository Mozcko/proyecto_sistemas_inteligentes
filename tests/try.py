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