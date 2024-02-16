import pygame
import time


def has_time_passed(start_time, border):
    return time.time() - start_time >= border


class Bird:
    def __init__(self, width, height, screen, filename_left="./images/bird_left.jpg", filename_right="./images/bird_right.jpg"):
        self.width = width
        self.height = height
        self.filename_right = filename_right
        self.filename_left = filename_left
        self.bird_image_right = pygame.transform.scale(
            pygame.image.load(filename_right).convert(), (width, height))
        self.bird_image_left = pygame.transform.scale(
            pygame.image.load(filename_left).convert(), (width, height))

        self.screen = screen
        self.bird_pos = pygame.Vector2(
            screen.get_width() / 2, screen.get_height() / 2)

        self.vel_y = 0  # Vertical velocity
        self.gravity = 700  # Gravity value (adjust as needed)
        self.last_time = time.time()

        self.direction = "right"

    def jump(self):
        self.vel_y = -700

    def move(self, keys, dt):

        current_time = time.time()
        self.bird_pos.y += 250 * dt

        if keys[pygame.K_a]:
            self.bird_pos.x -= 300 * dt
            self.direction = "left"
        if keys[pygame.K_d]:
            self.bird_pos.x += 300 * dt
            self.direction = "right"
        # Player can click to jump every 0.5 second
        if keys[pygame.K_SPACE] and has_time_passed(self.last_time, 0.5):
            self.last_time = current_time
            self.jump()

        # Update the bird's vertical position based on its velocity
        self.vel_y += self.gravity * dt
        self.bird_pos.y += self.vel_y * dt

        if (self.bird_pos.y >= self.screen.get_height()):
            self.bird_pos.y = 0

    def display(self):
        if self.direction == "right":
            self.screen.blit(self.bird_image_right, self.bird_pos)
        else:
            self.screen.blit(self.bird_image_left, self.bird_pos)
