import pygame

from src.config import CANVAS_HEIGHT, CANVAS_WIDTH, CANVAS_X_POSITION, CANVAS_Y_POSITION
from src.game.quadtree import Quadtree, Rectangle
import logging


class GameScene:
    def __init__(self, window):
        self.window = window
        quadtree_boundaries = Rectangle(
            CANVAS_X_POSITION, CANVAS_Y_POSITION, CANVAS_WIDTH, CANVAS_HEIGHT
        )
        logging.debug(self.window)
        self.quadtree = Quadtree(self.window, quadtree_boundaries, 8)
        self.quadtree.create_uniform_points(300)

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
        self.draw_dummy()

        self.draw_canvas_border()

        self.quadtree.draw()
        # self.quadtree.print_quadtree()

        pygame.display.update()

        # import ipdb;ipdb.set_trace()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
