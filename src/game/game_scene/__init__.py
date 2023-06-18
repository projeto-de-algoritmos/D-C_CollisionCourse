import random

import pygame

from src.config import CANVAS_HEIGHT, CANVAS_WIDTH, CANVAS_X_POSITION, CANVAS_Y_POSITION, POINT_RADIUS, NUMBER_OF_POINTS
from src.game.quadtree import Quadtree, Rectangle, Point


class GameScene:
    def __init__(self, window):
        self.window = window
        self.quadtree_boundaries = Rectangle(
            CANVAS_X_POSITION, CANVAS_Y_POSITION, CANVAS_WIDTH, CANVAS_HEIGHT
        )
        self.quadtree = Quadtree(self.window, self.quadtree_boundaries, 4)
        # self.quadtree.create_random_points(400)

        self.point_list = self.generate_point_list(NUMBER_OF_POINTS)

        for point in self.point_list:
            self.quadtree.insert(point)

    def generate_point_list(self, number_of_points):
        point_list = []
        for _ in range(number_of_points):
            point_list.append(
                Point(
                    random.randint(CANVAS_X_POSITION, CANVAS_X_POSITION + CANVAS_WIDTH),
                    random.randint(CANVAS_Y_POSITION, CANVAS_Y_POSITION + CANVAS_HEIGHT),
                )
            )

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

    def draw_dummy(self):
        pygame.draw.rect(self.window, (255, 0, 0), (0, 0, 100, 100))
        # draw random rect inside the window

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
        # clock.tick(60)

        while True:
            self.quadtree.clear()
            del self.quadtree
            self.quadtree = Quadtree(self.window, self.quadtree_boundaries, 2)

            for point in self.point_list:
                self.quadtree.insert(point)


            self.window.fill((0, 0, 0))

            # # Calculate FPS
            # fps = clock.get_fps()

            # # Render FPS
            # fps_text = font.render("FPS: " + str(int(fps)), True, (255, 255, 255))  # The color is white.

            # # Draw FPS
            # self.window.blit(fps_text, (10, 10))  # Draw at position (10, 10).

            self.draw_canvas_border()

            self.quadtree.draw()
            # self.quadtree.print_quadtree()

            pygame.display.update()

            # import ipdb;ipdb.set_trace()

        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
