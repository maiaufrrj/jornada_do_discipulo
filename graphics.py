# graphics.py
import os
import sys
import pygame
from config import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_image(image_path, size=(40, 40)):
    try:
        full_image_path = resource_path(image_path)
        image = pygame.image.load(full_image_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Warning: Could not load image: {image_path}. {e}")
        return None

# Carregar a imagem do item
item_image = load_image("images/item.png", size=(40, 40))

# Carregar a imagem do obstáculo
obstacle_image = load_image("images/obstacle.png", size=(40, 40))


def draw_objects(screen, items, obstacles):
    for item in items:
        if item_image:
            screen.blit(item_image, item.topleft)
        else:
            pygame.draw.rect(screen, (255, 255, 0), item)
    for obstacle in obstacles:
        if obstacle_image:
            screen.blit(obstacle_image, obstacle.topleft)
        else:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)