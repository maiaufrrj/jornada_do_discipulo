# graphics.py
import pygame

def load_image(image_path, size=(40, 40)):
    try:
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Warning: Could not load image: {image_path}. {e}")
        return None

def draw_objects(screen, items, obstacles, health_items, powerups):
    for item in items:
        pygame.draw.rect(screen, (255, 255, 0), item)
    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obstacle)
    for health_item in health_items:
        pygame.draw.rect(screen, (0, 255, 0), health_item)
    for powerup in powerups:
        pygame.draw.rect(screen, (0, 0, 255), powerup['rect'])
