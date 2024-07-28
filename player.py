import pygame
from config import *
import time

class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
        self.speed = PLAYER_BASE_SPEED
        self.radius = PLAYER_RADIUS
        self.velocity = pygame.math.Vector2(0, 0)
        self.health = INITIAL_HEALTH
#       self.start_time = 0
        self.shield_active = False
        self.shield_start_time = 0

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
            if self.shield_start_time == 0:
                self.shield_start_time = time.time()

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.velocity.x = 0
        if self.rect.top < 100:  # Espaço reservado para o texto da pergunta
            self.rect.top = 100
            self.velocity.y = 0
        if self.rect.bottom > SCREEN_HEIGHT - 100:  # Espaço reservado para o texto captado
            self.rect.bottom = SCREEN_HEIGHT - 100
            self.velocity.y = 0

    def draw(self, screen):
        pygame.draw.ellipse(screen, green, self.rect)

    # def move(self, keys):
    #     if keys[pygame.K_LEFT]:
    #         self.velocity.x = -self.speed
    #     elif keys[pygame.K_RIGHT]:
    #         self.velocity.x = self.speed
    #     else:
    #         self.velocity.x = 0
        
    #     if keys[pygame.K_UP]:
    #         self.velocity.y = -self.speed
    #     elif keys[pygame.K_DOWN]:
    #         self.velocity.y = self.speed
    #     else:
    #         self.velocity.y = 0

    #     if self.velocity.x != 0 or self.velocity.y != 0:
    #         if self.start_time == 0:
    #             self.start_time = time.time()

    #     self.rect.x += self.velocity.x
    #     self.rect.y += self.velocity.y

    #     if self.rect.left < 0:
    #         self.rect.left = 0
    #         self.velocity.x = 0
    #     if self.rect.right > SCREEN_WIDTH:
    #         self.rect.right = SCREEN_WIDTH
    #         self.velocity.x = 0
    #     if self.rect.top < 100:  # Espaço reservado para o texto da pergunta
    #         self.rect.top = 100
    #         self.velocity.y = 0
    #     if self.rect.bottom > SCREEN_HEIGHT - 100:  # Espaço reservado para o texto captado
    #         self.rect.bottom = SCREEN_HEIGHT - 100
    #         self.velocity.y = 0




