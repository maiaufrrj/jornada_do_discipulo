# player.py
import pygame
import time
from config import *

def move_player(player, speed, game_start_time):
    global player_velocity
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_velocity.x = -speed
    elif keys[pygame.K_RIGHT]:
        player_velocity.x = speed
    else:
        player_velocity.x = 0
    
    if keys[pygame.K_UP]:
        player_velocity.y = -speed
    elif keys[pygame.K_DOWN]:
        player_velocity.y = speed
    else:
        player_velocity.y = 0

    if player_velocity.x != 0 or player_velocity.y != 0:
        if game_start_time == 0:
            game_start_time = time.time()

    player.x += player_velocity.x
    player.y += player_velocity.y

    if player.left < 0:
        player.left = 0
        player_velocity.x = 0
    if player.right > screen_width:
        player.right = screen_width
        player_velocity.x = 0
    if player.top < 100:
        player.top = 100
        player_velocity.y = 0
    if player.bottom > screen_height - 100:
        player.bottom = screen_height - 100
        player_velocity.y = 0


class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width // 2, screen_height // 2, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
        self.speed = PLAYER_BASE_SPEED
        self.radius = PLAYER_RADIUS
        self.velocity = pygame.math.Vector2(0, 0)
        self.health = INITIAL_HEALTH
        self.start_time = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
        
        if keys[pygame.K_UP]:
            self.velocity.y = -self.speed
        elif keys[pygame.K_DOWN]:
            self.velocity.y = self.speed
        else:
            self.velocity.y = 0

        if self.velocity.x != 0 or self.velocity.y != 0:
            if self.start_time == 0:
                self.start_time = time.time()

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.velocity.x = 0
        if self.rect.top < 100:
            self.rect.top = 100
            self.velocity.y = 0
        if self.rect.bottom > screen_height - 100:
            self.rect.bottom = screen_height - 100
            self.velocity.y = 0
