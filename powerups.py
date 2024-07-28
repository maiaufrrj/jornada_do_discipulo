import time
import pygame
import random
from config import *
from utils import draw_text

class PowerUpManager:
    def __init__(self):
        self.active_powerups = []
        self.hourglass_image = self.load_hourglass_image()
        self.powerup_types = {
            "shield": {"color": blue, "duration": POWERUP_DURATION, "effect": "shield", "sound": "sounds/shield.wav"},
            "speed": {"color": red, "duration": POWERUP_DURATION, "effect": "speed", "sound": "sounds/speed.wav"},
            "freeze": {"color": cyan, "duration": POWERUP_DURATION, "effect": "freeze", "sound": "sounds/freeze.wav"},
            "points": {"color": orange, "duration": POWERUP_DURATION, "effect": "points", "sound": "sounds/points.wav"},
            "slow": {"color": purple, "duration": POWERUP_DURATION, "effect": "slow", "sound": "sounds/slow.wav"},
            "collect": {"color": pink, "duration": POWERUP_DURATION, "effect": "collect", "sound": "sounds/collect.wav"},
            "extra_life": {"color": yellow, "duration": 0, "effect": "extra_life", "sound": "sounds/extra_life.wav"},
            "explode": {"color": green, "duration": 0, "effect": "explode", "sound": "sounds/explode.wav"},
            "teleport": {"color": white, "duration": 0, "effect": "teleport", "sound": "sounds/teleport.wav"}
        }

    def load_hourglass_image(self):
        return pygame.image.load("images/hourglass.png")

    def create_powerups(self, level_num):
        powerups = []
        powerup_speeds = []
        powerup_directions = []
        for _ in range(MAX_POWERUPS_PER_LEVEL):
            powerup_rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), random.randint(100, SCREEN_HEIGHT - 120), 20, 20)
            powerups.append({"rect": powerup_rect, "type": random.choice(list(self.powerup_types.keys()))})
            powerup_speeds.append(random.uniform(1.0, 3.0))
            powerup_directions.append(pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])))
        return powerups, powerup_speeds, powerup_directions

    def apply_powerup_effect(self, powerup_type, player, obstacles, obstacle_speeds, obstacle_directions):
        start_time = time.time()
        if powerup_type == "shield":
            self.active_powerups.append({"type": "shield", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": self.hourglass_image})
        elif powerup_type == "speed":
            player.speed *= 1.5
            self.active_powerups.append({"type": "speed", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": self.hourglass_image})
        elif powerup_type == "freeze":
            self.active_powerups.append({"type": "freeze", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": self.hourglass_image})
        elif powerup_type == "points":
            self.active_powerups.append({"type": "points", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": self.hourglass_image})
        elif powerup_type == "slow":
            for i in range(len(obstacle_speeds)):
                obstacle_speeds[i] *= 0.1  # Reduz a velocidade dos obstáculos para 10% da atual
            self.active_powerups.append({"type": "slow", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": self.hourglass_image})
        elif powerup_type == "collect":
            player.radius *= 2
            self.active_powerups.append({"type": "collect", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": self.hourglass_image})
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

    def remove_powerup_effect(self, powerup, player, obstacles, obstacle_speeds, obstacle_directions):
        powerup_type = powerup["type"]
        if powerup_type == "speed":
            player.speed /= 1.5
        elif powerup_type == "slow":
            for i in range(len(obstacle_speeds)):
                obstacle_speeds[i] /= 0.1  # Restaura a velocidade dos obstáculos

    def update_powerups(self, player, obstacles, obstacle_speeds, obstacle_directions):
        for powerup in self.active_powerups[:]:
            if time.time() - powerup["start_time"] > powerup["duration"]:
                self.remove_powerup_effect(powerup, player, obstacles, obstacle_speeds, obstacle_directions)
                self.active_powerups.remove(powerup)

    def draw_powerups(self, screen):
        for powerup in self.active_powerups:
            remaining_time = powerup["duration"] - (time.time() - powerup["start_time"])
            if remaining_time > 0:
                draw_text(screen, f"{powerup['type']}: {int(remaining_time)}s", 24, 10, 60 + self.active_powerups.index(powerup) * 30, color=white, align="left")
