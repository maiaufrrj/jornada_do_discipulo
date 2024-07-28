import pygame
import random
from config import *
from powerups import *

def create_level(level_num, powerup_manager):
    global active_powerups

    active_powerups = []

    num_obstacles = 5 + level_num
    items = [pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), random.randint(100, SCREEN_HEIGHT - 120), 20, 20) for _ in range(5)]
    obstacles = [pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), random.randint(100, SCREEN_HEIGHT - 120), 20, 20) for _ in range(num_obstacles)]
    item_speeds = [random.uniform(1.0, 6.0) + 0.75 * level_num for _ in range(len(items))]
    obstacle_speeds = [random.uniform(1.0, 6.0) + 0.75 * level_num for _ in range(len(obstacles))]
    item_directions = [pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(len(items))]
    obstacle_directions = [pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(len(obstacles))]
    health_items = []

    powerups, powerup_speeds, powerup_directions = powerup_manager.create_powerups()

    return items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions, health_items, powerups, powerup_speeds, powerup_directions, "Level created"

def create_obstacle(obstacles, obstacle_speeds, obstacle_directions, level_num):
    new_obstacle = pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), random.randint(100, SCREEN_HEIGHT - 120), 20, 20)
    obstacles.append(new_obstacle)
    obstacle_speeds.append(random.uniform(1.0, 2.0) + 0.5 * level_num)
    obstacle_directions.append(pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])))
    return obstacles, obstacle_speeds, obstacle_directions

def move_objects(objects, speeds, directions):
    for i, obj in enumerate(objects):
        if isinstance(obj, dict):
            obj_rect = obj["rect"]
        else:
            obj_rect = obj
        
        obj_rect.x += speeds[i] * directions[i].x
        obj_rect.y += speeds[i] * directions[i].y
        
        if obj_rect.left < 0 or obj_rect.right > SCREEN_WIDTH:
            directions[i].x *= -1
        if obj_rect.top < 100 or obj_rect.bottom > SCREEN_HEIGHT - 100:
            directions[i].y *= -1
        
        for j in range(i + 1, len(objects)):
            if isinstance(objects[j], dict):
                other_rect = objects[j]["rect"]
            else:
                other_rect = objects[j]
            if obj_rect.colliderect(other_rect):
                directions[i].x *= -1
                directions[i].y *= -1
                directions[j].x *= -1
                directions[j].y *= -1

    return objects, speeds, directions

def handle_collisions(items, obstacles, item_speeds, obstacle_speeds, item_directions, obstacle_directions):
    for i, item in enumerate(items):
        for j, obstacle in enumerate(obstacles):
            if item.colliderect(obstacle):
                item_directions[i].x *= -1
                item_directions[i].y *= -1
                obstacle_directions[j].x *= -1
                obstacle_directions[j].y *= -1
