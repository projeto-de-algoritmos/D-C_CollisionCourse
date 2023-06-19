import math
import random

import pygame

from src.config import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    CANVAS_X_POSITION,
    CANVAS_Y_POSITION,
    POINT_RADIUS,
    NUMBER_OF_POINTS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    GAME_SETTINGS,
)
from src.game.quadtree import Quadtree, Rectangle, Point


class GameScene:
    def __init__(self, window):
        self.window = window
        self.quadtree_boundaries = Rectangle(
            CANVAS_X_POSITION, CANVAS_Y_POSITION, CANVAS_WIDTH, CANVAS_HEIGHT
        )
        self.quadtree = Quadtree(self.window, self.quadtree_boundaries, 2)
        # self.quadtree.create_random_points(400)

        self.point_list = self.generate_point_list(NUMBER_OF_POINTS)

        self.checks_per_frame = 0

        for point in self.point_list:
            self.quadtree.insert(point)

    def generate_point_list(self, number_of_points):
        point_list = []
        for _ in range(number_of_points):
            point_list.append(
                Point(
                    random.randint(CANVAS_X_POSITION, CANVAS_X_POSITION + CANVAS_WIDTH),
                    random.randint(
                        CANVAS_Y_POSITION, CANVAS_Y_POSITION + CANVAS_HEIGHT
                    ),
                )
            )

        radius = GAME_SETTINGS.get("easy").get("radius")

        for i in range(N):
            # Calculate the angle, then the x and y coordinates
            angle = i * 2 * math.pi / N
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            point_list.append(Point(x, y))

        # verify if there are any points that are too close to each other
        for point in point_list:
            for point2 in point_list:
                if point != point2:
                    if (
                        point.x - point2.x < POINT_RADIUS
                        and point.x - point2.x > -POINT_RADIUS
                        and point.y - point2.y < POINT_RADIUS
                        and point.y - point2.y > -POINT_RADIUS
                    ):
                        point_list.remove(point2)

        # verify if there are any points that are close to the border
        for point in point_list:
            if (
                point.x - CANVAS_X_POSITION < POINT_RADIUS
                or point.x - CANVAS_X_POSITION > CANVAS_WIDTH - POINT_RADIUS
                or point.y - CANVAS_Y_POSITION < POINT_RADIUS
                or point.y - CANVAS_Y_POSITION > CANVAS_HEIGHT - POINT_RADIUS
            ):
                point_list.remove(point)

        return point_list

    def draw_canvas_border(self):
        pygame.draw.rect(
            self.window,
            (0, 255, 0, 1),
            (CANVAS_X_POSITION, CANVAS_Y_POSITION, CANVAS_WIDTH, CANVAS_HEIGHT),
            1,
        )

    def run(self):
        clock = pygame.time.Clock()
        # self.draw_dummy()
        font = pygame.font.Font(None, 30)

        while True:
            clock.tick(60)

            # Clear the quadtree
            self.quadtree.clear()
            del self.quadtree

            # Build the quadtree
            self.quadtree = Quadtree(self.window, self.quadtree_boundaries, 2)

            # Insert the points into the quadtree
            for point in self.point_list:
                self.quadtree.insert(point)

            # Clear the window
            self.window.fill((0, 0, 0))

            # Calculate FPS
            fps = clock.get_fps()

            # Render FPS
            fps_text = font.render("FPS: " + str(int(fps)), True, (0, 255, 0))

            # Draw FPS
            self.window.blit(fps_text, (CANVAS_WIDTH + 10, 10))

            # Render checks per frame
            checks_per_frame_text = font.render(
                "Collision checks per frame: " + str(self.checks_per_frame),
                True,
                (0, 255, 0),
            )

            # Draw checks per frame
            self.window.blit(checks_per_frame_text, (CANVAS_WIDTH + 10, 40))

            # Reset checks per frame
            self.checks_per_frame = 0

            # Render point list size
            point_list_size_text = font.render(
                "Amount of points: " + str(len(self.point_list)), True, (0, 255, 0)
            )

            # Draw point list size
            self.window.blit(point_list_size_text, (CANVAS_WIDTH + 10, 70))

            self.draw_canvas_border()

            self.quadtree.draw()
            # self.quadtree.print_quadtree()

            for point in self.point_list:
                # Create a range around the airplane to check for collisions
                range = Rectangle(
                    point.x - point.collision_radius,
                    point.y - point.collision_radius,
                    point.collision_radius * 4,
                    point.collision_radius * 4,
                )

                # Query the quadtree for nearby airplanes
                nearby = self.quadtree.query_range(range)

                # Check for collisions with each nearby airplane
                for other in nearby:
                    self.checks_per_frame += 1
                    if (
                        point != other
                        and math.hypot(point.x - other.x, point.y - other.y)
                        < point.collision_radius + other.collision_radius
                    ):
                        # print(f"Collision detected between {point} and {other}")
                        point.collide(self.window)
                        other.collide(self.window)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
