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
        self.bird = None

        # Fruits
        self.fruits = None
        # Bombs and tnts
        self.bombs = None
        self.tnts = None

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

    def init_textures(self):
        # Create new instances
        self.bird = Bird(40, 40, self.screen)
        self.fruits = Fruits(self.screen)
        self.bombs = Bombs(
            self.screen, self.screen_width, self.screen_height)
        self.tnts = TNT(
            self.screen, self.screen_width, self.screen_height)

    def draw_menu(self, options, option_selected):
        WHITE = (255, 255, 255)
        rect_width = 200
        rect_height = 50
        rect_spacing = 50  # Spacing between rectangles
        num_options = len(options)
        # Calculate total height needed for all rectangles
        total_height = num_options * (rect_height + rect_spacing)
        # Calculate the starting y-coordinate for the first rectangle
        start_y = (self.screen_height - total_height) // 2 + 100

        # Load arrow image
        arrow_image = pygame.transform.scale(
            pygame.image.load("./images/arrow.png").convert_alpha(), (120, 70))

        self.screen.blit(self.start_background_image, (0, 0))
        display_text("Flying Bird", 110, self.screen_width / 2 -
                     20, 100, self.screen, self.title_font, (0, 0, 0))

        for i in range(num_options):
            rect_y = start_y + i * (rect_height + rect_spacing)
            pygame.draw.rect(self.screen, WHITE, (self.screen_width //
                                                  2 - rect_width // 2, rect_y, rect_width, rect_height))

            # Calculate position for text to be centered on the rectangle
            text_x = self.screen_width // 2
            text_y = rect_y + rect_height // 2

            display_text(options[i], 30, text_x, text_y,
                         self.screen, self.casual_font)

        # Draw arrow next to selected option
        arrow_y = start_y + (option_selected - 1) * \
            (rect_height + rect_spacing) + rect_height // 2 - 35
        self.screen.blit(arrow_image, (70, arrow_y))
        pygame.display.update()

    def congratulations_page(self, level_index):
        display_text(f"Congratulations for completing level {level_index}!",
                     64, self.screen_width / 2, self.screen_height / 2, self.screen, self.casual_font)

    def start_page(self):
        option = 1
        run = True
        texts = ["Play", "Instructions", "Quit"]

        rect_width = 200
        rect_height = 50
        rect_spacing = 50  # Spacing between rectangles
        num_rectangles = len(texts)
        # Calculate total height needed for all rectangles
        total_height = num_rectangles * (rect_height + rect_spacing)

        # Calculate the starting y-coordinate for the first rectangle
        start_y = (self.screen_height - total_height) // 2 + 150
        update = False
        initial = True

        # Load arrow image
        arrow_image = pygame.transform.scale(
            pygame.image.load("./images/arrow.png").convert_alpha(), (120, 70))

        while run:
            if update or initial:
                self.screen.blit(self.start_background_image, (0, 0))
                display_text("Flying Bird", 110, self.screen_width / 2,
                             100, self.screen, self.title_font, (0, 0, 0))
                initial = update = False
                extra = 0
                if option == 0:
                    extra = 1
                self.screen.blit(arrow_image, (70, start_y + (option - 1 + extra) *
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
                            self.running = True
                            self.init_textures()
                            return_value = self.game_loop()
                            if not return_value:
                                option = self.continue_page()
                            else:
                                self.congratulations_page(1)
                            update = True
                        elif option == 2:
                            pass
                        elif option == 3:
                            pass
                        elif option == 4:
                            self.instructions_page()
                            update = True
                        else:
                            pygame.quit()
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
        lines = ["Welcome in our Flying Bird game.", "In this game you have to fly with the bird", "and grab as much fruits as you can.",
                 "Try to avoid obstacles and collect", "power-ups to increase your score.", "Use arrow( ←, → ) keys to control the bird's movement.",
                 "Press the spacebar to make the bird flap", "its wings and gain altitude.", "Good luck and have fun playing!"]

        # Render and blit text
        font = pygame.font.Font(self.title_font, 65)
        instructions_surface = font.render(
            "Instructions", True, (255, 255, 255))
        instructions_rect = instructions_surface.get_rect(
            center=(self.screen_width // 2, 150))
        self.screen.blit(instructions_surface, instructions_rect)

        for i, line in enumerate(lines):
            display_text(line, 15, self.screen_width / 2 - len(line) / 2 + 30,
                         250 + i * 25, self.screen, self.casual_font, (255, 255, 255))
        display_text("Press enter to go back to the main page", 15, self.screen_width / 2 - len(line) / 2 + 20,
                     710, self.screen, self.casual_font, (255, 255, 255))

        # Update the display
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

    def continue_page(self):
        options = ["Play Again", "Main Page", "Quit"]
        option_selected = 1
        updated = True

        while True:
            if updated:
                self.draw_menu(options, option_selected)
                updated = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if option_selected == 1:
                            return 1
                        elif option_selected == 2:
                            return 0
                        elif option_selected == 3:
                            pygame.quit()
                    elif event.key == pygame.K_UP:
                        updated = True
                        option_selected = max(1, option_selected - 1)
                    elif event.key == pygame.K_DOWN:
                        updated = True
                        option_selected = min(
                            len(options), option_selected + 1)

    def game_loop(self, threshold=5000):
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

            # Draw & generate all textures
            self.fruits.generate()
            self.fruits.display()
            self.bombs.generate(self.bird.bird_pos)
            self.bombs.display()
            self.bombs.update()
            self.tnts.generate(self.bird.bird_pos)
            self.tnts.display()

            # Check for collisions
            fruit_collision = check_if_collision(
                self.bird.bird_pos, self.fruits.fruits)
            lost_bomb = check_if_collision(
                self.bird.bird_pos, self.bombs.items)
            lost_tnt = check_if_collision(
                self.bird.bird_pos, self.tnts.items)
            if lost_bomb != 0 or lost_tnt != 0:
                self.running = False
                return False

            # Display message if collision result is greater than 0 and for the specified duration
            if fruit_collision > 0:
                self.message = fruit_collision
                self.collision_time = time.time()
                self.bird.points += fruit_collision

            if self.message_duration > self.current_time - self.collision_time and self.message != 0:
                display_text(str(self.message), 25, self.bird.bird_pos.x + 20,
                             self.bird.bird_pos.y - 20, self.screen, self.casual_font, (255, 255, 255))
            else:
                self.message = 0
            display_text(f"{self.bird.points}/{threshold}", 50, self.screen_width /
                         2 + 20, 30, self.screen, self.casual_font)

            keys = pygame.key.get_pressed()
            self.bird.move(keys, self.dt)

            # flip() the display to put your work on screen
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

            # Based on our height decide if we have lost
            if self.bird.bird_pos.y >= self.screen_height:
                self.running = False
                return False

            # Decide if we have won
            if self.bird.points > 1000:
                return True
