import pygame

from src.config import CANVAS_HEIGHT, CANVAS_WIDTH, HUD_X_POSITION, HUD_Y_POSITION


class GameOver:

    def __init__(self, window, collision_point):
        self.window = window
        self.collision_point = collision_point
    
    def run(self):
        font = pygame.font.SysFont("Arial", 42)

        text = font.render("Game Over!", True, (0, 255, 0))

        self.window.blit(text, (HUD_X_POSITION, 100))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
