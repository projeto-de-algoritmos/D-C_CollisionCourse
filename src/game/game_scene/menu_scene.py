import math
import random
import logging

import pygame
from pygame.locals import *

from src.config import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    CANVAS_X_POSITION,
    CANVAS_Y_POSITION,
    POINT_RADIUS,
    NUMBER_OF_POINTS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    ASSETS_DIR
)
from src.game.quadtree import Quadtree, Rectangle, Point


class Button():
    def __init__(self, left, top, width, height, return_value):
        self.rect = pygame.Rect(left, top, width, height)
        self.return_value = return_value

    def check_click(self, event):
        # Checks if the provided event is a mouse click within this button's area
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.return_value
        return None


class MenuScene:
    def __init__(self, window):
        self.window = window
        self.menu_background = pygame.image.load(ASSETS_DIR + f'menu_{random.randint(1, 2)}.png').convert_alpha()
        
    def run(self):
        clock = pygame.time.Clock()
        
        font = pygame.font.Font(None, 30)

        while True:
            clock.tick(60)
            self.window.blit(self.menu_background, (0, 0))

            pygame.display.update()

            easy_button = Button(155, 547, 250, 100, 'easy')
            medium_button = Button(500, 547, 250, 100, 'medium')
            hard_button = Button(840, 547, 250, 100, 'hard')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif easy_button.check_click(event):
                    logging.info('Easy mode selected...')
                    return 'easy'
                elif medium_button.check_click(event):
                    logging.info('Medium mode selected...')
                    return 'medium'
                elif hard_button.check_click(event):
                    logging.info('Hard mode selected...')
                    return 'hard'
