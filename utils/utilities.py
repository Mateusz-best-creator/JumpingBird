import pygame
import time


def check_if_collision(bird_coordinates, items_data):
    items_to_remove = []

    collision = False

    for item in items_data:
        # Left side collision
        if (bird_coordinates.x + 40 > item["x_cor"] and
            bird_coordinates.x < item["x_cor"] and
            bird_coordinates.y + 40 > item["y_cor"] and
                bird_coordinates.y < item["y_cor"] + 40):
            items_to_remove.append(item)
            collision = True

        # Right side collision
        elif (bird_coordinates.x < item["x_cor"] + 40 and
              bird_coordinates.x + 40 > item["x_cor"] + 40 and
              bird_coordinates.y + 40 > item["y_cor"] and
                bird_coordinates.y < item["y_cor"] + 40):
            items_to_remove.append(item)
            collision = True

        # Top side collision
        elif (bird_coordinates.x + 40 > item["x_cor"] and
              bird_coordinates.x < item["x_cor"] + 40 and
              bird_coordinates.y + 40 > item["y_cor"] and
                bird_coordinates.y < item["y_cor"]):
            items_to_remove.append(item)
            collision = True

        # Bottom side collision
        elif (bird_coordinates.x + 40 > item["x_cor"] and
              bird_coordinates.x < item["x_cor"] + 40 and
              bird_coordinates.y < item["y_cor"] + 40 and
                bird_coordinates.y + 40 > item["y_cor"] + 40):
            items_to_remove.append(item)
            collision = True

    value = 0

    # Remove collided items
    for item in items_to_remove:
        items_data.remove(item)
        value += item["type"] * 100

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
