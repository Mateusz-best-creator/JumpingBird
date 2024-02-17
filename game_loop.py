import pygame
import time
from bird import Bird
from fruits import Fruits
from obstacles import Bombs, TNT
from utils.utilities import check_if_collision, display_text
import textwrap


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

        # Bombs and tnts
        self.bombs = Bombs(self.screen, self.screen_width, self.screen_height)
        self.tnts = TNT(self.screen, self.screen_width, self.screen_height)

        # Setting window title
        pygame.display.set_caption('Flying Bird')

        # background images
        self.game_background_image = pygame.image.load(
            "./images/game_background.png").convert()
        self.start_background_image = pygame.image.load(
            "./images/start_background.png").convert()

        self.current_time = time.time()
        self.start_time = time.time()
        self.collision_time = 0
        self.message_duration = 1
        self.message = 0

        self.casual_font = "./fonts/font.ttf"
        self.title_font = "./fonts/title.ttf"
        self.points = 0

    def start_page(self):
        option = 1
        run = True
        texts = ["Play", "Authenticate", "Hall Of Fame", "Instructions"]

        rect_width = 200
        rect_height = 50
        rect_spacing = 50  # Spacing between rectangles
        num_rectangles = len(texts)
        # Calculate total height needed for all rectangles
        total_height = num_rectangles * (rect_height + rect_spacing)

        # Calculate the starting y-coordinate for the first rectangle
        start_y = (self.screen_height - total_height) // 2
        update = False
        initial = True

        # Load arrow image
        arrow_image = pygame.transform.scale(
            pygame.image.load("./images/arrow.png").convert_alpha(), (120, 70))

        while run:
            if update or initial:
                self.screen.blit(self.start_background_image, (0, 0))
                display_text("Flying Bird", 110, self.screen_width / 2 -
                             20, 100, self.screen, self.title_font, (0, 0, 0))
                initial = update = False
                self.screen.blit(arrow_image, (70, start_y + (option - 1) *
                                 (rect_height + rect_spacing) + rect_height // 2 - 35))
                for i in range(num_rectangles):
                    rect_y = start_y + i * (rect_height + rect_spacing)
                    pygame.draw.rect(self.screen, (255, 255, 255), (self.screen_width //
                                                                    2 - rect_width // 2, rect_y, rect_width, rect_height))

                    # Calculate position for text to be centered on the rectangle
                    text_x = self.screen_width // 2
                    text_y = rect_y + rect_height // 2

                    display_text(texts[i], 30, text_x, text_y,
                                 self.screen, self.casual_font, (0, 0, 0))
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if option == 1:
                            self.bombs.bombs.clear()
                            self.tnts.tnts.clear()
                            self.game_loop()
                            update = True
                        elif option == 2:
                            pass
                        elif option == 3:
                            pass
                        else:
                            self.instructions_page()
                            update = True
                    elif event.key == pygame.K_UP:
                        option = max(1, option - 1)
                        update = True
                    elif event.key == pygame.K_DOWN:
                        option = min(num_rectangles, option + 1)
                        update = True

    def start_counter(self):
        # Fully transparent (RGBA color with alpha value 0)
        TRANSPARENT_GRAY = (100, 100, 100, 100)
        transparent_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA)
        transparent_surface.fill(TRANSPARENT_GRAY)

        # Play counter for 3 seconds
        start = time.time()
        while time.time() - start < 4:
            self.screen.blit(self.game_background_image, (0, 0))
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

    def instructions_page(self):
        WHITE = (255, 255, 255)
        GRAY = (110, 111, 112)
        # Text
        instructions_text = "Instructions"
        lines = ["Welcome in our Flying Bird game.", "In this game you have to fly with the bird", "and grab as much fruits as you can.",
                 "Try to avoid obstacles and collect", "power-ups to increase your score.", "Use the a, w, s, d keys to control the bird's movement.",
                 "Press the spacebar to make the bird flap", "its wings and gain altitude.", "Good luck and have fun playing!"]

        # Calculate rectangle dimensions
        rect_width = int(self.screen_width * 0.75)
        rect_height = self.screen_height - 100
        rect_x = (self.screen_width - rect_width) // 2
        rect_y = (self.screen_height - rect_height) // 2

        # Draw rectangle
        pygame.draw.rect(
            self.screen, GRAY, (rect_x, rect_y, rect_width, rect_height))

        # Render and blit text
        font = pygame.font.Font(self.title_font, 65)
        instructions_surface = font.render(instructions_text, True, WHITE)
        instructions_rect = instructions_surface.get_rect(
            center=(self.screen_width // 2, rect_y + 50))
        self.screen.blit(instructions_surface, instructions_rect)

        for i, line in enumerate(lines):
            display_text(line, 15, self.screen_width / 2 - len(line) / 2 + 30,
                         250 + i * 25, self.screen, self.casual_font, WHITE)
        display_text("Press enter to go back to the main page", 15, self.screen_width / 2 - len(line) / 2 + 20,
                     710, self.screen, self.casual_font, WHITE)

        # Update the display
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

    def game_loop(self):
        self.start_counter()

        while self.running:
            if (self.dt > 3):
                self.dt = 0.017
            self.current_time = time.time()

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Draw the background image
            self.screen.blit(self.game_background_image, (0, 0))
            # Draw bird texture
            self.bird.display()

            # Draw & generate fruits textures
            self.fruits.generate()
            self.fruits.display()
            self.bombs.generate(self.bird.bird_pos)
            self.bombs.display()
            self.bombs.update()
            self.tnts.generate(self.bird.bird_pos)
            self.tnts.display()

            # Check for collision
            result = check_if_collision(self.bird.bird_pos, self.fruits.fruits)
            lost_bomb = check_if_collision(
                self.bird.bird_pos, self.bombs.bombs)
            lost_tnt = check_if_collision(
                self.bird.bird_pos, self.tnts.tnts)
            if lost_bomb != 0 or lost_tnt != 0:
                self.running = False

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
            display_text(f"{self.points}/5000", 50, self.screen_width /
                         2 + 20, 30, self.screen, self.casual_font)

            keys = pygame.key.get_pressed()
            self.bird.move(keys, self.dt)

            # flip() the display to put your work on screen
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

            # Based on our height decide if we have lost
            if (self.bird.bird_pos.y >= self.screen_height):
                self.running = False
