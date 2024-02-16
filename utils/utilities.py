import pygame
import time


def check_if_collision(bird_coordinates, fruits_data, screen):
    fruits_to_remove = []

    collision = False

    for fruit in fruits_data:
        # Left side collision
        if (bird_coordinates.x + 40 > fruit["x_cor"] and
            bird_coordinates.x < fruit["x_cor"] and
            bird_coordinates.y + 40 > fruit["y_cor"] and
                bird_coordinates.y < fruit["y_cor"] + 40):
            fruits_to_remove.append(fruit)
            collision = True

        # Right side collision
        elif (bird_coordinates.x < fruit["x_cor"] + 40 and
              bird_coordinates.x + 40 > fruit["x_cor"] + 40 and
              bird_coordinates.y + 40 > fruit["y_cor"] and
                bird_coordinates.y < fruit["y_cor"] + 40):
            fruits_to_remove.append(fruit)
            collision = True

        # Top side collision
        elif (bird_coordinates.x + 40 > fruit["x_cor"] and
              bird_coordinates.x < fruit["x_cor"] + 40 and
              bird_coordinates.y + 40 > fruit["y_cor"] and
                bird_coordinates.y < fruit["y_cor"]):
            fruits_to_remove.append(fruit)
            collision = True

        # Bottom side collision
        elif (bird_coordinates.x + 40 > fruit["x_cor"] and
              bird_coordinates.x < fruit["x_cor"] + 40 and
              bird_coordinates.y < fruit["y_cor"] + 40 and
                bird_coordinates.y + 40 > fruit["y_cor"] + 40):
            fruits_to_remove.append(fruit)
            collision = True

    value = 0

    # Remove collided fruits
    for fruit in fruits_to_remove:
        fruits_data.remove(fruit)
        value += fruit["type"] * 100

    return value


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Function to display text for a specified duration
def display_text(message, font_size, x, y, screen, font_path, color=BLACK):
    # Set the font size
    font = pygame.font.Font(font_path, font_size)

    # Render the text with the specified font size
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    pygame.display.update()


def has_time_passed(start_time, border):
    return time.time() - start_time >= border
