import random
import math
import logging

import pygame


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 0), (self.x, self.y), 2)
        
    def __str__(self):
        return f"({self.x}, {self.y})"


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.left = x - width / 2
        self.right = x + width / 2
        self.top = y - height / 2
        self.bottom = y + height / 2

    def contains(self, point):
        return (
            point.x >= self.left
            and point.x <= self.right
            and point.y >= self.top
            and point.y <= self.bottom
        )

    def intersects(self, other):
        return not (
            other.left > self.right
            or other.right < self.left
            or other.top > self.bottom
            or other.bottom < self.top
        )
    
    def subdivide(self, quadrant):
        if quadrant == 'NE':
            return Rectangle(self.x + self.width / 4, self.y - self.height / 4, self.width / 2, self.height / 2)
        elif quadrant == 'NW':
            return Rectangle(self.x - self.width / 4, self.y - self.height / 4, self.width / 2, self.height / 2)
        elif quadrant == 'SE':
            return Rectangle(self.x + self.width / 4, self.y + self.height / 4, self.width / 2, self.height / 2)
        elif quadrant == 'SW':
            return Rectangle(self.x - self.width / 4, self.y + self.height / 4, self.width / 2, self.height / 2)
        
    def __str__(self):
        return f"({self.x}, {self.y}, {self.width}, {self.height})"


class Quadtree:
    def __init__(self, window, boundary: Rectangle, capacity: int):
        self.window = window
        self.point_list = []
        self.boundary = boundary
        self.capacity = capacity
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y

        self.northeast = Quadtree(
            self.window,
            self.boundary.subdivide('NE'),
            self.capacity
        )
        self.northwest = Quadtree(
            self.window,
            self.boundary.subdivide('NW'),
            self.capacity
        )
        self.southeast = Quadtree(
            self.window,
            self.boundary.subdivide('SE'),
            self.capacity
        )
        self.southwest = Quadtree(
            self.window,
            self.boundary.subdivide('SW'),
            self.capacity
        )
        self.divided = True
            

    def insert(self, point):
        if not self.boundary.contains(point):
            logging.info(f"POINT OUTSIDE BOUNDARY: {point}")
            logging.info(f"BOUNDARY: {self.boundary}")
            return False

        if len(self.point_list) < self.capacity:
            self.point_list.append(point)
            return True

        else:
            if not self.divided:
                if len(self.point_list) < self.capacity:
                    self.point_list.append(point)
                    return True

                self.subdivide()

        return (
            self.northeast.insert(point) or
            self.northwest.insert(point) or
            self.southeast.insert(point) or
            self.southwest.insert(point)
        )
    
    def create_random_points(self, amount):
        for i in range(amount):
            self.insert(
                Point(
                    random.randint(
                        self.boundary.x, self.boundary.x + self.boundary.width
                    ),
                    random.randint(
                        self.boundary.y, self.boundary.y + self.boundary.height
                    ),
                )
            )

    def create_random_gaussian_points(self, amount):
        for i in range(amount):
            coords = (
                random.gauss(
                    self.boundary.x + self.boundary.width / 2, self.boundary.width / 2
                ),
                random.gauss(
                    self.boundary.y + self.boundary.height / 2, self.boundary.height / 2
                ),
            )
            logging.debug(f"Creating point at {coords}")
            self.insert(Point(abs(coords[0]), abs(coords[1])))

    def create_normal_points(self, amount):
        for i in range(amount):
            coords = (
                random.normalvariate(
                    self.boundary.x + self.boundary.width / 2, self.boundary.width / 2
                ),
                random.normalvariate(
                    self.boundary.y + self.boundary.height / 2, self.boundary.height / 2
                ),
            )
            print(f"Creating point at {coords}")
            self.insert(Point(abs(coords[0]), abs(coords[1])))
    
    def create_uniform_points(self, amount):
        for i in range(amount):
            coords = (
                random.uniform(
                    self.boundary.x, self.boundary.x + self.boundary.width
                ),
                random.uniform(
                    self.boundary.y, self.boundary.y + self.boundary.height
                ),
            )
            print(f"Creating point at {coords}")
            self.insert(Point(abs(coords[0]), abs(coords[1])))

    def draw(self):
        pygame.draw.rect(
            self.window,
            (0, 255, 0),
            (
                self.boundary.x,
                self.boundary.y,
                self.boundary.width,
                self.boundary.height,
            ),
            1,
        )

        for point in self.point_list:
            point.draw(self.window)

        if self.divided:
            self.northwest.draw()
            self.northeast.draw()
            self.southwest.draw()
            self.southeast.draw()

    def print_quadtree(self):
        print(
            self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height
        )
        print(f"Len: {len(self.point_list)}")
        for point in self.point_list:
            print(f"({point.x}, {point.y}) // ")

        if self.divided:
            self.northwest.print_quadtree()
            self.northeast.print_quadtree()
            self.southwest.print_quadtree()
            self.southeast.print_quadtree()
