import pygame
import time
from bird import Bird
from fruits import Fruits
from utils.utilities import check_if_collision, display_text


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

        # background image
        self.background_image = pygame.image.load(
            "./images/background.png").convert()

        self.current_time = time.time()
        self.start_time = time.time()
        self.collision_time = 0
        self.message_duration = 1
        self.message = 0

        self.casual_font = pygame.font.Font("./fonts/font.ttf", 25)
        self.title_font = pygame.font.Font("./fonts/title.ttf", 75)
        self.points = 0

    # Create entire start page UI
    def start_page(self):
        option = 1
        run = True
        while run:
            self.screen.blit(self.background_image, (0, 0))
            display_text("Flying Bird", 100, self.screen_width / 2 -
                         60, 30, self.screen, self.title_font, (255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                run = False
            elif keys[pygame.K_UP]:
                if option != 1:
                    option -= 1
            elif keys[pygame.K_DOWN]:
                if option != 4:
                    option += 1

        self.game_loop()

    def start_counter(self):
        # Fully transparent (RGBA color with alpha value 0)
        TRANSPARENT_GRAY = (100, 100, 100, 100)
        transparent_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA)
        transparent_surface.fill(TRANSPARENT_GRAY)

        # Play counter for 3 seconds
        start = time.time()
        while time.time() - start < 4:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(transparent_surface, (0, 0))
            time_to_display = int(time.time() - start)
            if (time_to_display == 0):
                time_to_display = 3
            elif time_to_display == 1:
                time_to_display = 2
            elif time_to_display == 2:
                time_to_display = 1
            else:
                time_to_display = "START"

            display_text(str(time_to_display), 100, self.screen_width /
                         2, self.screen_height / 2, self.screen, self.casual_font)
            pygame.display.update()  # Update the display outside the loop

    def game_loop(self):
        self.start_counter()

        while self.running:
            if (self.dt > 3):
                self.dt -= 3
            self.current_time = time.time()

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Draw the background image
            self.screen.blit(self.background_image, (0, 0))
            # Draw bird texture
            self.bird.display()

            # Draw & generate fruits textures
            self.fruits.generate()
            self.fruits.display()

            # Check for collision
            result = check_if_collision(
                self.bird.bird_pos, self.fruits.fruits, self.screen)

            # Display message if collision result is greater than 0 and for the specified duration
            if result > 0:
                self.message = result
                self.collision_time = time.time()
                self.points += result

            if self.message_duration > self.current_time - self.collision_time and self.message != 0:
                display_text(str(self.message), 25, self.bird.bird_pos.x + 20,
                             self.bird.bird_pos.y - 20, self.screen, self.casual_font, (255, 255, 255))
            else:
                self.message = 0
            display_text(f"{self.points}", 50, self.screen_width /
                         2, 30, self.screen, self.casual_font)

            keys = pygame.key.get_pressed()
            self.bird.move(keys, self.dt)

            # flip() the display to put your work on screen
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

            # Based on our height decide if we have lost
            if (self.bird.bird_pos.y >= self.screen_height):
                self.running = False
