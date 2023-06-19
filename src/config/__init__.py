import os

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

CANVAS_WIDTH = 700
CANVAS_HEIGHT = 700

CANVAS_X_POSITION = 25
CANVAS_Y_POSITION = 25

NUMBER_OF_POINTS = 100
POINT_RADIUS = 25
VELOCITY = 0.8
INVALID_VELOCITIES = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
VELOCITY_MIN_VALUE = 0.2
VELOCITY_MAX_VALUE = 1.0

HUD_X_POSITION = CANVAS_X_POSITION + CANVAS_WIDTH + 25
HUD_Y_POSITION = CANVAS_Y_POSITION

ASSETS_DIR =  os.path.join(os.path.dirname(__file__) + "/../assets/")

GAME_SETTINGS = {
    "easy": {
        "number_of_points": 4,
        "velocity": 0.4,
        "generation_radius": 200,
        "spawn_rate": 1,
    }
}
