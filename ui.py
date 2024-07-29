# ui.py
import pygame
import time
from utils import *
from config import *
from graphics import *

def show_main_menu(screen):
    menu_options = ["Iniciar a Partida", "Ajuda", "Melhores Pontuações", "Sair"]
    selected_option = 0
    font = pygame.font.Font(pygame.font.match_font('arial'), 36)

    while True:
        screen.fill(black)
        draw_text(screen, "Menu Principal", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, white, align="center")

        for i, option in enumerate(menu_options):
            color = white if i != selected_option else green
            draw_text(screen, option, 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 50, color=color, align="center")

        pygame.display.flip()
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == "Iniciar a Partida":
                        return
                    elif menu_options[selected_option] == "Ajuda":
                        show_rules(screen)
                    elif menu_options[selected_option] == "Melhores Pontuações":
                        show_high_scores(screen)
                    elif menu_options[selected_option] == "Sair":
                        pygame.quit()
                        exit()

def show_congratulations_screen(screen, congratulations_image_file):
    congratulations_image = load_image(congratulations_image_file, size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(congratulations_image, (0, 0))
    pygame.display.flip()
    time.sleep(10)

def show_rules(screen):
    try:
        with open(help_file, "r", encoding="utf-8") as f:
            rules = f.read().split('\n')
    except FileNotFoundError:
        rules = ["Arquivo de ajuda não encontrado."]
    
    screen.fill(black)
    y_offset = 100
    for line in rules:
        draw_text(screen, line, 24, SCREEN_WIDTH // 2, y_offset, align="center", max_width=SCREEN_WIDTH - 40)
        y_offset += 30

    draw_text(screen, "Pressione Enter para voltar ao menu", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, align="center")
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        pygame.time.Clock().tick(30)

def show_high_scores(screen):
    high_scores = load_high_scores()
    screen.fill(black)
    draw_text(screen, "Melhores Pontuações", 48, SCREEN_WIDTH // 2, 50, align="center")

    y_offset = 150
    for score, date in high_scores:
        draw_text(screen, f"{score} - {date}", 36, SCREEN_WIDTH // 2, y_offset, align="center")
        y_offset += 40

    draw_text(screen, "Pressione Enter para voltar ao menu", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, align="center")
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        pygame.time.Clock().tick(30)

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

def show_game_over_screen(screen, score, collision_count, level_num, correct_answers, correct_answers_streak, high_scores):

    save_high_scores(score, high_scores)

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

def show_pause_menu(screen):
    menu_options = ["Continuar", "Reiniciar", "Sair"]
    selected_option = 0
    font = pygame.font.Font(pygame.font.match_font('arial'), 36)

    while True:
        screen.fill(black)
        draw_text(screen, "Menu de Pausa", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, color=white, align="center")

        for i, option in enumerate(menu_options):
            color = white if i != selected_option else green
            draw_text(screen, option, 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 50, color=color, align="center")

        pygame.display.flip()
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == "Continuar":
                        return
                    elif menu_options[selected_option] == "Reiniciar":
                        # Reinicia o jogo
                        return "restart"
                    elif menu_options[selected_option] == "Sair":
                        pygame.quit()
                        exit()

def draw_text(screen, text, size, x, y, color=(255, 255, 255), align="center", max_width=None):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    if max_width:
        words = text.split(' ')
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            if align == "center":
                text_rect.midtop = (x, y + i * size)
            elif align == "left":
                text_rect.topleft = (x, y + i * size)
            elif align == "right":
                text_rect.topright = (x, y + i * size)
            screen.blit(text_surface, text_rect)
    else:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.midtop = (x, y)
        elif align == "left":
            text_rect.topleft = (x, y)
        elif align == "right":
            text_rect.topright = (x, y)
        screen.blit(text_surface, text_rect)

def reset_game():
    global player, player_health, level_num, items, obstacles, item_speeds, obstacle_speeds, item_directions, obstacle_directions, health_items, powerups, powerup_speeds, powerup_directions, message, score, health_spawn_time, current_question
    global high_scores, collision_count, correct_answers, correct_answers_streak, player_speed, player_radius, player_velocity, game_start_time, start_time, last_item_collect_time, answered_questions, active_powerups, running
    
    running = True

    # Reinicializar variáveis do jogo
    player = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
    player_health = INITIAL_HEALTH
    level_num = INITIAL_LEVEL
    items, obstacles, item_speeds, obstacle_speeds, item_directions, obstacle_directions, health_items, powerups, powerup_speeds, powerup_directions, message = create_level(level_num)
    score = INITIAL_SCORE
    health_spawn_time = time.time()
    current_question = None
    high_scores = load_high_scores()
    collision_count = INITIAL_COLLISION_COUNT
    correct_answers = INITIAL_CORRECT_ANSWERS
    correct_answers_streak = INITIAL_CORRECT_ANSWERS_STREAK
    player_speed = PLAYER_BASE_SPEED
    player_radius = PLAYER_RADIUS
    player_velocity = pygame.math.Vector2(0, 0)
    game_start_time = GAME_START_TIME
    start_time = INITIAL_START_TIME
    last_item_collect_time = INITIAL_LAST_ITEM_COLLECT_TIME
    answered_questions = set()
    active_powerups = []

