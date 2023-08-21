import logging
import asyncio

import pygame
import argparse
from pygame.locals import *

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.game.game_scene.demo import DemoGameScene
from src.game.game_scene.game import GameScene
from src.game.game_scene.menu_scene import MenuScene

logging.basicConfig(level=logging.INFO)


async def main():
    logging.info("Initializing pygame...")

    game_over_command = 'menu'

    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    args = parser.parse_args()

    # true if --demo, false if not
    demo = args.demo

    try:
        pygame.init()

        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        while True:
            if demo:
                game_scene = DemoGameScene(window)
            else:
                if game_over_command == 'menu':
                    menu = MenuScene(window)
                    difficulty = menu.run()
                game_scene = GameScene(window, difficulty)

            game_over_command = game_scene.run()

            await asyncio.sleep(0)

            if game_over_command == 'quit':
                return            


    except Exception as e:
        logging.exception(e)
        pygame.quit()
        raise e


logging.info("Starting game...")
asyncio.run(main())
