import pygame
import random
import time
from config import *
from utils import *

def load_image(image_path, size=(40, 40)):
    try:
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Warning: Could not load image: {image_path}. {e}")
        return None

def load_hourglass_image():
    try:
        hourglass_image = pygame.image.load("images/hourglass.png")
        return pygame.transform.scale(hourglass_image, (40, 40))
    except pygame.error as e:
        print(f"Warning: Could not load image: images/hourglass.png. {e}")
        return None

hourglass_image = load_hourglass_image()

powerup_images = {
    "shield": load_image("images/shield.png", size=(40, 40)),
    "speed": load_image("images/speed.png", size=(40, 40)),
    "freeze": load_image("images/freeze.png", size=(40, 40)),
    "points": load_image("images/points.png", size=(40, 40)),
    "slow": load_image("images/slow.png", size=(40, 40)),
    "collect": load_image("images/collect.png", size=(40, 40)),
    "extra_life": load_image("images/extra_life.png", size=(40, 40)),
    "explode": load_image("images/explode.png", size=(40, 40)),
    "teleport": load_image("images/teleport.png", size=(40, 40))
}

powerup_types = {
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

active_powerups = []

def draw_text(screen, text, size, x, y, color=white, align="center"):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.midtop = (x, y)
    elif align == "left":
        text_rect.topleft = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)
    screen.blit(text_surface, text_rect)

def draw_active_powerups(screen):
    global active_powerups
    current_time = time.time()
    for i, powerup in enumerate(active_powerups):
        remaining_time = POWERUP_DURATION - (current_time - powerup["start_time"])
        if powerup.get("hourglass_image"):
            screen.blit(powerup["hourglass_image"], (screen_width - 50, 10 + 50 * i))
        draw_text(screen, f"{int(remaining_time)}s", 24, screen_width - 60, 20 + 50 * i, align="right")

class PowerUpManager:
    def __init__(self):
        self.active_powerups = []

    def create_powerup(self, x, y, powerup_type):
        rect = pygame.Rect(x, y, 30, 30)
        hourglass_image = load_hourglass_image()
        powerup = {
            "type": powerup_type,
            "rect": rect,
            "start_time": time.time(),
            "duration": POWERUP_DURATION,
            "hourglass_image": hourglass_image
        }
        return powerup

    def apply_powerup_effect(self, powerup, player, obstacles, obstacle_speeds, obstacle_directions):
        powerup_type = powerup["type"]
        start_time = time.time()
        hourglass_image = load_hourglass_image()

        if powerup_type == "shield":
            self.active_powerups.append({"type": "shield", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": hourglass_image})
        elif powerup_type == "speed":
            player.speed *= 1.5
            self.active_powerups.append({"type": "speed", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": hourglass_image})
        elif powerup_type == "freeze":
            self.active_powerups.append({"type": "freeze", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": hourglass_image})
        elif powerup_type == "points":
            self.active_powerups.append({"type": "points", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": hourglass_image})
        elif powerup_type == "slow":
            for i in range(len(obstacle_speeds)):
                obstacle_speeds[i] *= 0.1  # Reduz a velocidade dos obstáculos para 10% da atual
            self.active_powerups.append({"type": "slow", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": hourglass_image})
        elif powerup_type == "collect":
            player.radius *= 2
            self.active_powerups.append({"type": "collect", "start_time": start_time, "duration": POWERUP_DURATION, "hourglass_image": hourglass_image})
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
            player.rect.x = random.randint(0, screen_width - player.rect.width)
            player.rect.y = random.randint(100, screen_height - player.rect.height - 100)

        sound_path = powerup_types[powerup_type]["sound"]
        play_sound(sound_path)

    def update_powerups(self, player, obstacles, obstacle_speeds, obstacle_directions):
        current_time = time.time()
        for powerup in self.active_powerups[:]:
            if current_time - powerup["start_time"] >= powerup["duration"]:
                self.remove_powerup_effect(powerup, player, obstacles, obstacle_speeds, obstacle_directions)
                self.active_powerups.remove(powerup)

    def remove_powerup_effect(self, powerup, player, obstacles, obstacle_speeds, obstacle_directions):
        powerup_type = powerup["type"]
        if powerup_type == "speed":
            player.speed /= 1.5
        elif powerup_type == "slow":
            for i in range(len(obstacle_speeds)):
                obstacle_speeds[i] /= 0.1  # Restaura a velocidade dos obstáculos

    def draw_powerups(self, screen):
        for powerup in self.active_powerups:
            screen.blit(powerup["hourglass_image"], (powerup["rect"].x, powerup["rect"].y))