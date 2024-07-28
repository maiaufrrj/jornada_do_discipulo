# ui.py
import pygame
import time
from utils import draw_text
from config import *

def show_start_screen(screen):
    start_time = time.time()
    countdown = TIME_TO_START
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

def save_high_scores(scores):
    with open(score_file, "w", encoding="utf-8") as f:
        for score, date in scores:
            f.write(f"{score},{date}\n")


def show_game_over_screen(screen, score, collision_count, level_num, correct_answers, correct_answers_streak, high_scores):

    # Atualiza os melhores scores
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")
    high_scores.append([str(score), date_str])
    high_scores = sorted(high_scores, key=lambda x: int(x[0]), reverse=True)[:10]
    save_high_scores(high_scores)

    screen.fill((0, 0, 0))
    SCREEN_WIDTH, SCREEN_HEIGHT
    draw_text(screen, "Game Over", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, color=(255, 0, 0), align="center")
    draw_text(screen, f"Colisões: {collision_count}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, color=(255, 255, 255), align="center")
    draw_text(screen, f"Nível alcançado: {level_num}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, color=(255, 255, 255), align="center")
    draw_text(screen, f"Respostas corretas: {correct_answers}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, color=(255, 255, 255), align="center")
    draw_text(screen, f"Maior sequência de acertos: {correct_answers_streak}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, color=(255, 255, 255), align="center")
    draw_text(screen, "Pressione Enter para voltar ao menu", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, color=(255, 255, 255), align="center")

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
        pygame.time.Clock().tick(30)

