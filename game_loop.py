import pygame
from bird import Bird
from fruits import Fruits
from collisions import check_if_collision


class Game:
    def __init__(self, screen_width, screen_height):
        # Screen dimensions
        self.screen_height = screen_height
        self.screen_width = screen_width

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        # Rectangles properties
        self.rect_color = (139, 69, 19)  # Brown color (RGB)

        # Create bird instance
        self.bird = Bird(40, 40, self.screen)

        # Fruits
        self.fruits = Fruits(self.screen)

        # Setting window title
        pygame.display.set_caption('Flying Bird')

    def game_loop(self):
        while self.running:

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("white")

            # Draw bird texture
            self.bird.display()

            # Draw & generate fruits textures
            self.fruits.generate()
            self.fruits.display()

            check_if_collision(self.bird.bird_pos, self.fruits.fruits)

            # Draw rectangles that will be the borders of the screen
            pygame.draw.rect(self.screen, self.rect_color,
                             (0, 0, self.screen_width, 15))
            pygame.draw.rect(self.screen, self.rect_color,
                             (0, self.screen_height - 15, self.screen_width, 15))

            keys = pygame.key.get_pressed()
            self.bird.move(keys, self.dt)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000
