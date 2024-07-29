import time
import pygame
import random
from config import *
from utils import draw_text
import math

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

    def create_powerup_rect(self):
        return pygame.Rect(random.randint(0, SCREEN_WIDTH - 40), random.randint(100, SCREEN_HEIGHT - 140), 40, 40)

    def create_powerups(self):
        powerup_list = list(self.powerup_types.keys())
        powerup_list.remove("extra_life")

        random_powerups = random.sample(powerup_list, 2)
        powerups = [{"type": p, "rect": self.create_powerup_rect(), "color": self.powerup_types[p]["color"]} for p in random_powerups]
        powerup_speeds = [random.uniform(1.0, 3.0) for _ in range(2)]
        powerup_directions = [pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(2)]

        return powerups, powerup_speeds, powerup_directions

    def create_extra_life(self):
        extra_life = {"type": "extra_life", "rect": self.create_powerup_rect(), "color": self.powerup_types["extra_life"]["color"]}
        return extra_life

    def apply_powerup_effect(self, powerup_type, player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions):

        def find_furthest_point(player, obstacles, screen_width, screen_height):
            max_distance = -1
            best_x, best_y = player.rect.x, player.rect.y
            
            for _ in range(1000):  # Teste um número grande de posições aleatórias
                x = random.randint(0, screen_width - player.rect.width)
                y = random.randint(100, screen_height - player.rect.height - 100)
                min_distance = min(math.sqrt((x - obs.x) ** 2 + (y - obs.y) ** 2) for obs in obstacles)
                
                if min_distance > max_distance:
                    max_distance = min_distance
                    best_x, best_y = x, y
                    
            return best_x, best_y
        
        def teleport_player(player, obstacles, screen, screen_width, screen_height):
            best_x, best_y = find_furthest_point(player, obstacles, screen_width, screen_height)
            player.rect.x = best_x
            player.rect.y = best_y

            for _ in range(10):  # Pisca 20 vezes
                screen.fill((0, 0, 0))  # Limpa a tela
                pygame.draw.rect(screen, player.color, player.rect)  # Desenha o jogador
                pygame.display.flip()  # Atualiza a tela
                pygame.time.delay(100)  # Pausa por 0,05 segundo
                screen.fill((0, 0, 0))  # Limpa a tela novamente
                pygame.display.flip()  # Atualiza a tela
                pygame.time.delay(100)  # Pausa por 0,05 segundo

            time.sleep(0.2)  # Pausa o movimento de tudo por 0,5 segundos adicionais (totalizando 0,7 segundos)

        start_time = time.time()
        
        if powerup_type in self.powerup_types:
            self.active_powerups.append({"rect": pygame.Rect(0, 0, 0, 0), "type": powerup_type, "start_time": start_time, "duration": POWERUP_DURATION})
        
        if powerup_type == "speed":
            player.speed *= 1.5

        elif powerup_type == "freeze":
            for i in range(len(item_speeds)):
                item_speeds[i] *= 0.1  # Reduz a velocidade dos itens para 10% da atual
        
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
            teleport_player(player, obstacles, screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        elif powerup_type == "shield":
            player.shield_active = True
            player.shield_start_time = start_time


    def remove_powerup_effect(self, powerup, player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions):
        powerup_type = powerup["type"]
        
        if powerup_type == "speed":
            player.speed /= 1.5
        
        elif powerup_type == "slow":
            for i in range(len(obstacle_speeds)):
                obstacle_speeds[i] /= 0.1 # Restaura a velocidade dos obstáculos
        
        elif powerup_type == "freeze":
            for i in range(len(item_speeds)):
                item_speeds[i] /= 0.1  # Restaura a velocidade original dos itens
        
        elif powerup_type == "shield":
            player.shield_active = False

    def update_powerups(self, player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions):
        # Iterar sobre os power-ups ativos
        for powerup in self.active_powerups[:]:
            # Verificar se é um power-up de vida extra e se ainda não foi gerado
            if powerup["type"] == "extra_life" and not powerup.get("spawned"):
                # Gerar o power-up de vida extra se o jogador tiver perdido vida
                if player.health < INITIAL_HEALTH:
                    powerup["spawned"] = True
                    powerup["rect"].topleft = (random.randint(0, SCREEN_WIDTH - 40), random.randint(100, SCREEN_HEIGHT - 140))
                    self.active_powerups.append(powerup)
            # Verificar se a duração do power-up expirou
            if time.time() - powerup["start_time"] > self.powerup_types[powerup["type"]]["duration"]:
                # Remover o efeito do power-up e removê-lo da lista de ativos
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
