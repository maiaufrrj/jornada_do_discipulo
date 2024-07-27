# graphics.py
import pygame

def load_image(image_path, size=(40, 40)):
    try:
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Warning: Could not load image: {image_path}. {e}")
        return None
