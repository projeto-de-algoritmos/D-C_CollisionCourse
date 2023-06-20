import pygame
import logging

from src.config import CANVAS_HEIGHT, CANVAS_WIDTH, HUD_X_POSITION, HUD_Y_POSITION


class GameOver:

    def __init__(self, window, collision_point):
        self.window = window
        self.collision_point = collision_point
    
    def run(self):
        font = pygame.font.SysFont(None, 42)

        text = font.render("GAME OVER", True, (0, 255, 0))

        self.window.blit(text, (120, 755))

        text = font.render("Press 'Space' to retry", True, (0, 255, 0))

        self.window.blit(text, (350, 755))

        text = font.render("Press 'Arrow Down' to exit", True, (0, 255, 0))

        self.window.blit(text, (700, 755))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        logging.info('Restarting game...')
                        return 'retry'
                    if event.key == pygame.K_DOWN:
                        logging.info('Exiting game...')
                        return 'menu'
                    
