class Node:
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.parent = parent

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
