import logging

import moderngl
import pygame
from pygame.locals import *

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.game.game_scene.demo import DemoGameScene
from src.game.game_scene.game import GameScene

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Initializing pygame...")

    try:
        pygame.init()

        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF|OPENGL)

        while True:
            game_scene = GameScene(window)
            #game_scene = DemoGameScene(window)
            game_scene.run()

    except Exception as e:
        logging.exception(e)
        pygame.quit()
        raise e


if __name__ == "__main__":
    logging.info("Starting game...")
    main()
