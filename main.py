from game_loop import Game
import pygame

if __name__ == "__main__":
    game = Game(600, 800) # width, height
    game.game_loop()
    pygame.quit()