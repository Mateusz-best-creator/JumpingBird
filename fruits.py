import pygame
import random
import time
from bird import has_time_passed

fruit_data = {
    1: {"filename": "./images/fruit1.png", "name": "apple", "value": 10},
    2: {"filename": "./images/fruit2.png", "name": "orange", "value": 20},
    3: {"filename": "./images/fruit3.png", "name": "cherry", "value": 30}
}


class Fruits:
    def __init__(self, screen, delta=2, max_fruits=8):
        self.max_fruits = max_fruits
        self.current_fruits = 0
        self.fruits = []
        self.screen = screen
        self.delta = delta
        self.last_time = time.time()
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.fruit_images = {key: pygame.transform.scale(pygame.image.load(value["filename"]).convert_alpha(), (40, 40))
                             for key, value in fruit_data.items()}

    def generate(self):
        if self.current_fruits >= self.max_fruits:
            return
        current_time = time.time()
        if has_time_passed(self.last_time, self.delta):
            self.current_fruits += 1
            self.last_time = current_time
            new_index = len(self.fruits)
            new_x_coordinate = random.uniform(20, self.screen_width - 100)
            new_y_coordinate = random.uniform(20, self.screen_height - 100)
            type = random.choice(list(fruit_data.keys()))
            print("New index: ", new_index)
            self.fruits.append({"type": type, "index": new_index,
                                "x_cor": new_x_coordinate, "y_cor": new_y_coordinate})

    def display(self):
        for fruit in self.fruits:
            self.screen.blit(self.fruit_images[fruit["type"]],
                             (fruit["x_cor"], fruit["y_cor"]))
