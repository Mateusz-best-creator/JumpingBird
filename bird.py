import pygame
import time

def has_time_passed(start_time):
    return time.time() - start_time >= 0.5

class Bird:
    def __init__(self, width, height, screen, filename = "./bird.jpg"):
        self.width = width
        self.height = height
        self.filename = filename
        self.image = pygame.transform.scale(pygame.image.load(filename).convert(), (width, height))
        
        self.screen = screen
        self.bird_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

        self.vel_y = 0  # Vertical velocity
        self.gravity = 550  # Gravity value (adjust as needed)
        self.last_time = time.time()

    def jump(self):
        self.vel_y = -700

    def move(self, keys, dt):

        current_time = time.time()
        self.bird_pos.y += 250 * dt

        if keys[pygame.K_a]:
            self.bird_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            self.bird_pos.x += 300 * dt
        if keys[pygame.K_SPACE] and has_time_passed(self.last_time):
            self.last_time = current_time
            self.jump()

        # Update the bird's vertical position based on its velocity
        self.vel_y += self.gravity * dt
        self.bird_pos.y += self.vel_y * dt

        if (self.bird_pos.y >= self.screen.get_height()):
            self.bird_pos.y = 0



    def draw(self):
        self.screen.blit(self.image, self.bird_pos)