import pygame
import random
import math
import time
from utils.utilities import has_time_passed


class Bombs:
    def __init__(self, screen, screen_width, screen_height, max_bombs=5):
        self.max_bombs = max_bombs
        self.bombs = []
        self.current_bombs = 0
        self.delta = 2.5
        self.screen = screen
        self.last_time = time.time()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bomb_image = pygame.transform.scale(pygame.image.load(
            "./images/bomb.png").convert_alpha(), (40, 40))

    def generate(self, bird_position):
        if self.current_bombs >= self.max_bombs:
            return
        current_time = time.time()
        if has_time_passed(self.last_time, self.delta):
            self.last_time = current_time
            # Minimum distance between bomb and bird
            min_distance = 100
            while True:
                new_x_coordinate = random.uniform(20, self.screen_width - 100)
                new_y_coordinate = random.uniform(
                    100, self.screen_height - 100)
                # Calculate distance between bomb and bird
                distance = math.sqrt(
                    (new_x_coordinate - bird_position.x) ** 2 + (new_y_coordinate - bird_position.y) ** 2)
                if distance >= min_distance:
                    break
            generated_time = time.time()
            self.bombs.append(
                {"type": 1, "time": generated_time, "x_cor": new_x_coordinate, "y_cor": new_y_coordinate})
            self.current_bombs += 1

    def update(self):
        now = time.time()
        for bomb in self.bombs:
            # If bomb is longer than 10 seconds on the board we want to remove it
            if now - bomb["time"] > 10:
                self.bombs.remove(bomb)
        self.current_bombs = len(self.bombs)

    def display(self):
        for bomb in self.bombs:
            self.screen.blit(self.bomb_image,
                             (bomb["x_cor"], bomb["y_cor"]))
        self.current_bombs = len(self.bombs)
