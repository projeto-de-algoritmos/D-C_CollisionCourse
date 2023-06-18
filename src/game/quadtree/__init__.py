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

    def contains(self, point):
        return (
            point.x >= self.x
            and point.x <= self.x + self.width
            and point.y >= self.y
            and point.y <= self.y + self.height
        )

    def intersects(self, other):
        return not (
            self.x + self.width <= other.x
            or self.y + self.height <= other.y
            or self.x >= other.x + other.width
            or self.y >= other.y + other.height
        )
        
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
        width = self.boundary.width
        height = self.boundary.height

        self.northwest = Quadtree(
            self.window,
            Rectangle(x, y, math.ceil(width / 2), math.ceil(height / 2)),
            self.capacity,
        )
        self.northeast = Quadtree(
            self.window,
            Rectangle(
                x + math.ceil(width / 2), y, math.ceil(width / 2), math.ceil(height / 2)
            ),
            self.capacity,
        )
        self.southwest = Quadtree(
            self.window,
            Rectangle(
                x,
                y + math.ceil(height / 2),
                math.ceil(width / 2),
                math.ceil(height / 2),
            ),
            self.capacity,
        )
        self.southeast = Quadtree(
            self.window,
            Rectangle(
                x + math.ceil(width / 2),
                y + math.ceil(height / 2),
                math.ceil(width / 2),
                math.ceil(height / 2),
            ),
            self.capacity,
        )

        for point in self.point_list:
            if not (
                self.northwest.insert(point) or
                self.northeast.insert(point) or
                self.southwest.insert(point) or
                self.southeast.insert(point)
            ):
                logging.error(f'No quadrant found for point {point}')

        self.point_list = []

        self.divided = True

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

    def insert(self, point):
        if not self.boundary.contains(point):
            logging.debug(f"POINT OUTSIDE BOUNDARY: {point}")
            logging.debug(f"BOUNDARY: {self.boundary}")
            return False

        if len(self.point_list) < self.capacity and not self.divided:
            self.point_list.append(point)
            return True

        else:
            if not self.divided:
                self.subdivide()

            if self.northwest.insert(point):
                return True
            elif self.northeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            else:
                logging.error(f'No quadrant found for point {point}')
                return False

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
