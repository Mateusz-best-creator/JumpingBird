import pygame
from bird import Bird

class Game:
    def __init__(self, screen_width, screen_height):
        # Screen dimensions
        self.screen_height = screen_height
        self.screen_width = screen_width

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)

        # Rectangles properties
        self.rect_color = (139, 69, 19)  # Brown color (RGB)
        self.rect_x = 10
        self.rect_y = 100
        self.rect_width = 20
        self.rect_height = 100

        # Create bird instance
        self.bird = Bird(50, 50, self.screen)
        
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

            self.bird.draw()
            pygame.draw.circle(self.screen, "red", self.player_pos, 40)
            # Draw rectangles that will be the borders of the screen
            pygame.draw.rect(self.screen, self.rect_color, (0, 0, 15, self.screen_height))
            pygame.draw.rect(self.screen, self.rect_color, (self.screen_width - 15, 0, 15, self.screen_height))
            pygame.draw.rect(self.screen, self.rect_color, (0, 0, self.screen_width, 15))
            pygame.draw.rect(self.screen, self.rect_color, (0, self.screen_height - 15, self.screen_width, 15))

            keys = pygame.key.get_pressed()
            self.bird.move(keys, self.dt)
            if keys[pygame.K_w]:
                self.player_pos.y -= 300 * self.dt
            if keys[pygame.K_s]:
                self.player_pos.y += 300 * self.dt
            if keys[pygame.K_a]:
                self.player_pos.x -= 300 * self.dt
            if keys[pygame.K_d]:
                self.player_pos.x += 300 * self.dt

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

game = Game(600, 800) # width, height
game.game_loop()
pygame.quit()