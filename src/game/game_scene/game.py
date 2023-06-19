import math
import random
import logging
import time

import moderngl
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
    GAME_SETTINGS,
)
from src.game.quadtree import Quadtree, Rectangle, Point
from src.game.game_scene.game_over import GameOver

ctx = moderngl.create_context(standalone=True)

# Shader programs
prog = ctx.program(
    vertex_shader='''
        #version 330

        in vec2 in_vert;
        in vec3 in_color;

        out vec3 color;

        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            color = in_color;
        }
    ''',
    fragment_shader='''
        #version 330

        in vec3 color;

        out vec4 fragColor;

        uniform float time;
        uniform vec2 resolution;

        void main() {
            float scanline = sin(gl_FragCoord.y * 3.14159 / 2.0 + time * 2.0) * 0.5 + 0.5;
            fragColor = vec4(color * scanline, 1.0);
        }
    ''',
)

# Full screen rectangle vertices and colors
vertices = ctx.buffer(
    b'\x00\x00\x00\x00\xff\x00\x00' +  # Vertex 1: Position and color
    b'\xff\x00\x00\x00\x00\xff\x00' +  # Vertex 2: Position and color
    b'\xff\xff\x00\x00\x00\x00\xff' +  # Vertex 3: Position and color
    b'\x00\xff\x00\x00\xff\xff\xff'    # Vertex 4: Position and color
)

# Vertex array object
vao = ctx.simple_vertex_array(prog, vertices, 'in_vert', 'in_color')

class GameState:
    PLAYING = 1
    SPAWNING = 2


class GameScene:
    
    center_x = CANVAS_HEIGHT / 2
    center_y = CANVAS_WIDTH / 2

    def __init__(self, window):
        self.window = window
        self.quadtree_boundaries = Rectangle(
            CANVAS_X_POSITION, CANVAS_Y_POSITION, CANVAS_WIDTH, CANVAS_HEIGHT
        )
        self.quadtree = Quadtree(self.window, self.quadtree_boundaries, 2)
        self.checks_per_frame = 0
        self.amount_of_points = GAME_SETTINGS.get("easy").get("number_of_points")
        self.generation_radius = GAME_SETTINGS.get("easy").get("generation_radius")
        self.collision_point = None

        self.point_list = self.generate_point_list(NUMBER_OF_POINTS)
        for point in self.point_list:
            self.quadtree.insert(point)



    def generate_point_list(self, number_of_points):
        point_list = []
        
        for i in range(self.amount_of_points):
            # Calculate the angle, then the x and y coordinates
            angle = i * 2 * math.pi / self.amount_of_points
            x = self.center_x + self.generation_radius * math.cos(angle)
            y = self.center_y + self.generation_radius * math.sin(angle)
            point_list.append(Point(x, y))

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

    def draw_canvas_border(self):
        pygame.draw.rect(
            self.window,
            (0, 255, 0, 1),
            (CANVAS_X_POSITION, CANVAS_Y_POSITION, CANVAS_WIDTH, CANVAS_HEIGHT),
            1,
        )

    def check_collision(self, point):
        # Create a range around the airplane to check for collisions
        range = Rectangle(
            point.x - point.collision_radius,
            point.y - point.collision_radius,
            point.collision_radius * 4,
            point.collision_radius * 4,
        )

        # Query the quadtree for nearby airplanes
        nearby = self.quadtree.query_range(range)

        # Check for collisions with each nearby airplane
        for other in nearby:
            self.checks_per_frame += 1
            if (
                point != other
                and math.hypot(point.x - other.x, point.y - other.y)
                < point.collision_radius + other.collision_radius
            ):
                logging.info(f"Collision detected between {point} and {other}")
                point.collide(self.window)
                other.collide(self.window)
                return True
            
    def spawn_point(self):
        quadtree = self.quadtree
        window = self.window

        while True:
            new_point = Point(
                random.randint(CANVAS_X_POSITION + (POINT_RADIUS * 2), CANVAS_X_POSITION + CANVAS_WIDTH - (POINT_RADIUS * 2)),
                random.randint(CANVAS_Y_POSITION + (POINT_RADIUS * 2), CANVAS_Y_POSITION + CANVAS_HEIGHT - (POINT_RADIUS * 2)),
            )
            # Check if new point is far from existing points.
            spawn_region = Rectangle(new_point.x - new_point.danger_radius,
                                    new_point.y - new_point.danger_radius,
                                    2 * new_point.danger_radius,
                                    2 * new_point.danger_radius)
            points_near_spawn = quadtree.query_range(spawn_region)

            if not points_near_spawn:
                break

        
        new_point.draw_spawn(window)
        update_area = new_point.get_area_rect()

        pygame.display.flip()
        
        time.sleep(1)

        return new_point

    def run(self):
        game_state = GameState.PLAYING
        running = True

        clock = pygame.time.Clock()
        
        font = pygame.font.Font(None, 30)

        max_spawn_rate = 5 

        last_spawn_time = time.time()

        spawn_rate = GAME_SETTINGS.get("easy").get("spawn_rate") 

        spawn_rate_increase = (max_spawn_rate - spawn_rate) / 600 

        while running:
            clock.tick(60)

            # Set the uniform values
            prog['time'].value = time.time()  # Pass the current time
            prog['resolution'].value = (WINDOW_WIDTH, WINDOW_HEIGHT)  # Pass the window dimensions


            # Clear the quadtree
            self.quadtree.clear()
            del self.quadtree

            # Build the quadtree
            self.quadtree = Quadtree(self.window, self.quadtree_boundaries, 2)

            # Insert the points into the quadtree
            for point in self.point_list:
                self.quadtree.insert(point)

            # Clear the window
            self.window.fill((0, 0, 0))

            # Calculate FPS
            fps = clock.get_fps()

            # Render FPS
            fps_text = font.render("FPS: " + str(int(fps)), True, (0, 255, 0))

            # Draw FPS
            self.window.blit(fps_text, (CANVAS_WIDTH + 10, 10))

            # Render checks per frame
            checks_per_frame_text = font.render(
                "Collision checks per frame: " + str(self.checks_per_frame),
                True,
                (0, 255, 0),
            )

            # Draw checks per frame
            self.window.blit(checks_per_frame_text, (CANVAS_WIDTH + 10, 40))

            # Reset checks per frame
            self.checks_per_frame = 0

            # Render point list size
            point_list_size_text = font.render(
                "Amount of points: " + str(len(self.point_list)), True, (0, 255, 0)
            )

            # Draw point list size
            self.window.blit(point_list_size_text, (CANVAS_WIDTH + 10, 70))

            current_time = time.time()
            elapsed_time = current_time - last_spawn_time

            if game_state == GameState.PLAYING:
                self.draw_canvas_border()

                self.quadtree.draw()

                for point in self.point_list:
                    self.collision_point = self.check_collision(point) or self.collision_point
                    
                pygame.display.flip()

                if self.collision_point:
                    self.game_over = GameOver(self.window, self.collision_point)
                    self.game_over.run()
                    return
                
                if elapsed_time >= 10/spawn_rate:  # It's time to spawn a new point
                    game_state = GameState.SPAWNING
                    last_spawn_time = current_time  # Reset the last spawn time
                    spawn_rate = min(max_spawn_rate, spawn_rate + spawn_rate_increase * elapsed_time)
                
            elif game_state == GameState.SPAWNING:
                new_point = self.spawn_point()
                self.point_list.append(new_point)
                game_state = GameState.PLAYING


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_region = Rectangle(mouse_pos[0] - Point.danger_radius, mouse_pos[1] - Point.danger_radius, 
                                            2 * Point.danger_radius, 2 * Point.danger_radius)
                    points_in_clicked_region = self.quadtree.query_range(clicked_region)
                    for point in points_in_clicked_region:
                        if point.is_within_danger_radius(mouse_pos):
                            point.invert_velocity()

