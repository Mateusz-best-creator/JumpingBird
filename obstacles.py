import pygame
import random
import math
import time
from utils.utilities import has_time_passed
import abc


class Obstacles(abc.ABC):
    def __init__(self, screen, screen_width, screen_height, delta, filename, time):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.items = []
        self.delta = delta
        self.item_image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(), (40, 40))
        self.last_time = time
        self.current_items = 0

    @abc.abstractmethod
    def generate(self, bird_position):
        pass

    @abc.abstractmethod
    def display(self):
        pass


class Bombs(Obstacles):
    def __init__(self, screen, screen_width, screen_height, max_bombs=5):
        super().__init__(screen, screen_width, screen_height,
                         2.5, "./images/bomb.png", time.time())
        self.max_bombs = max_bombs

    def generate(self, bird_position):
        if self.current_items >= self.max_bombs or time.time() - self.last_time < 5:
            return
        current_time = time.time()
        print(current_time)
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
            self.items.append(
                {"type": 1, "time": generated_time, "x_cor": new_x_coordinate, "y_cor": new_y_coordinate})
            self.current_items += 1

    def update(self):
        now = time.time()
        for bomb in self.items:
            # If bomb is longer than 10 seconds on the board we want to remove it
            if now - bomb["time"] > 10:
                self.items.remove(bomb)
        self.current_items = len(self.items)

    def display(self):
        for bomb in self.items:
            self.screen.blit(self.item_image,
                             (bomb["x_cor"], bomb["y_cor"]))
        self.current_items = len(self.items)


class TNT(Obstacles):
    def __init__(self, screen, screen_width, screen_height, max_tnt=2):
        super().__init__(screen, screen_width, screen_height,
                         5, "./images/tnt.png", time.time())
        self.max_tnts = max_tnt
        self.velocity = 1

    def generate(self, bird_position):
        if self.current_items >= self.max_tnts:
            return
        current_time = time.time()
        if has_time_passed(self.last_time, self.delta) and current_time >= 5:
            self.last_time = current_time
            # Minimum distance between bomb and bird
            min_distance = 50
            while True:
                new_y_coordinate = 0
                new_x_coordinate = random.uniform(
                    50, self.screen_width - 50)
                # Calculate distance between bomb and bird
                distance = new_x_coordinate - bird_position.x
                if distance >= min_distance:
                    break
            generated_time = time.time()
            self.items.append(
                {"type": 1, "time": generated_time, "x_cor": new_x_coordinate, "y_cor": new_y_coordinate})
            self.current_items += 1

    def display(self):
        for tnt in self.items:
            tnt["y_cor"] += self.velocity
            self.screen.blit(self.item_image, (tnt["x_cor"], tnt["y_cor"]))
            if (tnt["y_cor"] >= self.screen_height):
                self.items.remove(tnt)
        self.current_items = len(self.items)
