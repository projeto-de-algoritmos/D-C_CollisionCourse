import pygame

from src.config import CANVAS_HEIGHT, CANVAS_WIDTH, CANVAS_X_POSITION, CANVAS_Y_POSITION


class GameScene:
    
    def __init__(self, window):
        self.window = window
        
    def draw_dummy(self):
        pygame.draw.rect(self.window, (255, 0, 0), (0, 0, 100, 100))
        # draw random rect inside the window
        
    def draw_canvas_border(self):
        pygame.draw.rect(self.window, (0, 255, 0, 1), (CANVAS_X_POSITION, CANVAS_Y_POSITION, CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    
    def run(self):
        
        self.draw_dummy()
        
        self.draw_canvas_border()
        
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return