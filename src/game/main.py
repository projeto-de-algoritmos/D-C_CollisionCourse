import logging

import pygame

from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.game.game_scene import GameScene

logging.basicConfig(level=logging.INFO)


def main():
    logging.info('Initializing pygame...')
    
    try:
        pygame.init()
        
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        while True:
            game_scene = GameScene(window)
        
            game_scene.run()
            
    except Exception as e:
        logging.exception(e)
        pygame.quit()
        raise e            
        
        
if __name__ == '__main__':
    logging.info('Starting game...')
    main()