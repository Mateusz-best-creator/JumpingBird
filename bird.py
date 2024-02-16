import pygame
import time


class Bird:
    def __init__(self, width, height, screen, filename_left="./images/bird_left.png", filename_right="./images/bird_right.png"):
        self.width = width
        self.height = height
        self.filename_right = filename_right
        self.filename_left = filename_left
        self.bird_image_right = pygame.transform.scale(
            pygame.image.load(filename_right).convert_alpha(), (width, height))
        self.bird_image_left = pygame.transform.scale(
            pygame.image.load(filename_left).convert_alpha(), (width, height))

        self.screen = screen
        self.bird_pos = pygame.Vector2(screen.get_width() / 2, 0)

        self.vel_y = 0  # Vertical velocity
        self.gravity = 700  # Gravity value (adjust as needed)
        self.last_jump_time = 0

        self.direction = "right"

    def jump(self):
        self.vel_y = -500
        self.last_jump_time = time.time()

    def move(self, keys, dt):
        self.bird_pos.y += self.vel_y * dt

        if keys[pygame.K_a]:
            self.bird_pos.x -= 300 * dt
            self.direction = "left"
        if keys[pygame.K_d]:
            self.bird_pos.x += 300 * dt
            self.direction = "right"

        # Player can jump every 0.5 second
        if keys[pygame.K_SPACE] and time.time() - self.last_jump_time >= 0.5:
            self.jump()

        # Apply gravity
        self.vel_y += self.gravity * dt
        # Screen edge handling
        if self.bird_pos.x > self.screen.get_width():
            self.bird_pos.x = 0
        elif self.bird_pos.x < -self.width:
            self.bird_pos.x = self.screen.get_width()

    def display(self):
        if self.direction == "right":
            self.screen.blit(self.bird_image_right, self.bird_pos)
        else:
            self.screen.blit(self.bird_image_left, self.bird_pos)
