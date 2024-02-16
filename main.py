from game_loop import Game
import pygame

if __name__ == "__main__":
    game_loop = Game(600, 800)  # width, height
    game_loop.game_loop()
    pygame.quit()
