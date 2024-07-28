import time
import pygame
import random
from config import *
from utils import draw_text

class PowerUpManager:
    def __init__(self):
        self.active_powerups = []
        self.powerup_types = {
            "shield": {"color": blue, "duration": POWERUP_DURATION, "effect": "shield", "sound": "sounds/shield.wav", "image": self.load_powerup_image("shield")},
            "speed": {"color": red, "duration": POWERUP_DURATION, "effect": "speed", "sound": "sounds/speed.wav", "image": self.load_powerup_image("speed")},
            "freeze": {"color": cyan, "duration": POWERUP_DURATION, "effect": "freeze", "sound": "sounds/freeze.wav", "image": self.load_powerup_image("freeze")},
            "points": {"color": orange, "duration": POWERUP_DURATION, "effect": "points", "sound": "sounds/points.wav", "image": self.load_powerup_image("points")},
            "slow": {"color": purple, "duration": POWERUP_DURATION, "effect": "slow", "sound": "sounds/slow.wav", "image": self.load_powerup_image("slow")},
            "collect": {"color": pink, "duration": POWERUP_DURATION, "effect": "collect", "sound": "sounds/collect.wav", "image": self.load_powerup_image("collect")},
            "extra_life": {"color": yellow, "duration": 0, "effect": "extra_life", "sound": "sounds/extra_life.wav", "image": self.load_powerup_image("extra_life")},
            "explode": {"color": green, "duration": 0, "effect": "explode", "sound": "sounds/explode.wav", "image": self.load_powerup_image("explode")},
            "teleport": {"color": white, "duration": 0, "effect": "teleport", "sound": "sounds/teleport.wav", "image": self.load_powerup_image("teleport")}
        }

    def load_powerup_image(self, powerup_type):
        image = pygame.image.load(f"images/{powerup_type}.png")
        return pygame.transform.scale(image, (40, 40))

    def create_powerups(self):
        powerups = []
        powerup_speeds = []
        powerup_directions = []
        for _ in range(MAX_POWERUPS_PER_LEVEL):
            powerup_rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), random.randint(100, SCREEN_HEIGHT - 120), 20, 20)
            powerup_type = random.choice(list(self.powerup_types.keys()))
            powerups.append({"rect": powerup_rect, "type": powerup_type})
            powerup_speeds.append(random.uniform(1.0, 3.0))
            powerup_directions.append(pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])))
        return powerups, powerup_speeds, powerup_directions

    def apply_powerup_effect(self, powerup_type, player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions):
        start_time = time.time()
        if powerup_type in self.powerup_types:
            self.active_powerups.append({"rect": pygame.Rect(0, 0, 0, 0), "type": powerup_type, "start_time": start_time, "duration": POWERUP_DURATION})
        if powerup_type == "speed":
            player.speed *= 1.5
        elif powerup_type == "slow":
            for i in range(len(obstacle_speeds)):
                obstacle_speeds[i] *= 0.1  # Reduz a velocidade dos obstáculos para 10% da atual
        elif powerup_type == "collect":
            player.radius *= 2
        elif powerup_type == "extra_life":
            player.health += 1
        elif powerup_type == "explode":
            num_obstacles_to_remove = min(3, len(obstacles))
            for _ in range(num_obstacles_to_remove):
                idx = random.randint(0, len(obstacles) - 1)
                obstacles.pop(idx)
                obstacle_speeds.pop(idx)
                obstacle_directions.pop(idx)
        elif powerup_type == "teleport":
            player.rect.x = random.randint(0, SCREEN_WIDTH - player.rect.width)
            player.rect.y = random.randint(100, SCREEN_HEIGHT - player.rect.height - 100)

        elif powerup_type == "shield":
            player.shield_active = True
            player.shield_start_time = start_time


    def remove_powerup_effect(self, powerup, player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions):
        powerup_type = powerup["type"]
        if powerup_type == "speed":
            player.speed /= 1.5
        elif powerup_type == "slow":
            for i in range(len(obstacle_speeds)):
                obstacle_speeds[i] /= 0.1  # Restaura a velocidade dos obstáculos
        elif powerup_type == "freeze":
            for i in range(len(item_speeds)):
                item_speeds[i] /= 0.01  # Restaura a velocidade original dos itens
        elif powerup_type == "shield":
            player.shield_active = False


    def update_powerups(self, player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions):
        for powerup in self.active_powerups[:]:
            if time.time() - powerup["start_time"] > powerup["duration"]:
                self.remove_powerup_effect(powerup, player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions)
                self.active_powerups.remove(powerup)


    def draw_powerups(self, screen, powerups):
        for powerup in powerups:
            screen.blit(self.powerup_types[powerup["type"]]["image"], (powerup["rect"].x, powerup["rect"].y))

    def draw_active_powerups(self, screen):
        for index, powerup in enumerate(self.active_powerups):
            remaining_time = powerup["duration"] - (time.time() - powerup["start_time"])
            if remaining_time > 0:
                draw_text(screen, f"{powerup['type']}: {int(remaining_time)}s", 35, 10, SCREEN_HEIGHT - 90 - (index * 30), color=green, align="left")
