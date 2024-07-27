# ui.py
import pygame
import time
from utils import draw_text

def show_start_screen(screen):
    start_time = time.time()
    countdown = 5
    font = pygame.font.Font(pygame.font.match_font('arial'), 36)
    while True:
        screen.fill((0, 0, 0))
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = max(0, countdown - int(elapsed_time))
        
        if remaining_time == 0:
            break

        draw_text(screen, f"Preparando para começar! ({remaining_time})", 36, screen.get_width() // 2, screen.get_height() // 2 - 50, align="center")

        pygame.display.flip()
        pygame.time.Clock().tick(30)
