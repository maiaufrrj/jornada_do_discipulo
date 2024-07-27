# utils.py
import pygame
import time
import random
import pandas as pd
from config import *
from level import *

def play_sound(sound_path):
    if sound_path:  # Verificar se sound_path não é None
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
        except pygame.error as e:
            print(f"Warning: Could not play sound: {sound_path}. {e}")
    else:
        print("Warning: No sound path provided")

# def load_sound(sound_path):
#     try:
#         return pygame.mixer.Sound(sound_path)
#     except pygame.error as e:
#         print(f"Warning: Could not load sound: {sound_path}. {e}")
#         return None

def draw_text(screen, text, size, x, y, color, align="center", max_width=None):
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

def load_high_scores():
    try:
        with open(score_file, "r", encoding="utf-8") as f:
            return [line.strip().split(",") for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

def save_high_scores(scores):
    with open(score_file, "w", encoding="utf-8") as f:
        for score, date in scores:
            f.write(f"{score},{date}\n")

def load_questions():
    try:
        df = pd.read_excel(question_file)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return [
            {"pergunta": "Qual é o maior mandamento?", "opcao_1": "Amar a Deus sobre todas as coisas", "opcao_2": "Não matar", "opcao_3": "Guardar o sábado", "opcao_4": "Não roubar", "resposta": "1"}
        ]

def show_question(screen, question, selected_option=None, is_correct=None):
    option_colors = [white, white, white, white]
    if selected_option is not None:
        if is_correct:
            option_colors[selected_option - 1] = green
        else:
            option_colors[selected_option - 1] = red
    draw_text(screen, question["pergunta"], 24, screen_width // 2, 70, align="center", max_width=screen_width - 40)
    draw_text(screen, f"1. {question['opcao_1']}", 24, screen_width // 2, 110, color=option_colors[0], align="center", max_width=screen_width - 40)
    draw_text(screen, f"2. {question['opcao_2']}", 24, screen_width // 2, 150, color=option_colors[1], align="center", max_width=screen_width - 40)
    draw_text(screen, f"3. {question['opcao_3']}", 24, screen_width // 2, 190, color=option_colors[2], align="center", max_width=screen_width - 40)
    draw_text(screen, f"4. {question['opcao_4']}", 24, screen_width // 2, 230, color=option_colors[3], align="center", max_width=screen_width - 40)

def check_answer(question, answer):
    correct_answer = str(question["resposta"]).strip()
    received_answer = str(answer).strip()
    return correct_answer == received_answer

def get_random_question(questions, answered_questions):
    available_questions = [q for q in questions if q["pergunta"] not in answered_questions]
    if not available_questions:
        return None
    question = random.choice(available_questions)
    return question

def show_congratulations_screen(screen, congratulations_image, zerou_sound):
    screen.blit(congratulations_image, (0, 0))
    if zerou_sound:
        zerou_sound.play()  # Tocar som de "zerou" quando o jogo for completado
    pygame.display.flip()
    time.sleep(30)

def show_start_screen(screen):
    start_time = time.time()
    countdown = TIME_TO_START
    while True:
        screen.fill(black)
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = max(0, countdown - int(elapsed_time))
        
        if remaining_time == 0:
            break

        draw_text(screen, f"Preparando para começar! ({remaining_time})", 36, screen_width // 2, screen_height // 2 - 50, color=white, align="center")

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def show_pause_menu(screen):
    menu_options = ["Continuar", "Reiniciar", "Sair"]
    selected_option = 0
    font = pygame.font.Font(pygame.font.match_font('arial'), 36)

    while True:
        screen.fill(black)
        draw_text(screen, "Menu de Pausa", 48, screen_width // 2, screen_height // 2 - 100, color=white, align="center")

        for i, option in enumerate(menu_options):
            color = white if i != selected_option else green
            draw_text(screen, option, 36, screen_width // 2, screen_height // 2 - 50 + i * 50, color=color, align="center")

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

def reset_game():
    global player, player_health, level_num, items, obstacles, item_speeds, obstacle_speeds, item_directions, obstacle_directions, health_items, powerups, powerup_speeds, powerup_directions, message, score, health_spawn_time, current_question
    global high_scores, collision_count, correct_answers, correct_answers_streak, player_speed, player_radius, player_velocity, game_start_time, start_time, last_item_collect_time, answered_questions, active_powerups, running
    
    running = True

    # Reinicializar variáveis do jogo
    player = pygame.Rect(screen_width // 2, screen_height // 2, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
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

def show_main_menu(screen):
    menu_options = ["Iniciar a Partida", "Ajuda", "Melhores Pontuações", "Sair"]
    selected_option = 0
    font = pygame.font.Font(pygame.font.match_font('arial'), 36)

    while True:
        screen.fill(black)
        draw_text(screen, "Menu Principal", 48, screen_width // 2, screen_height // 2 - 100, white, align="center")

        for i, option in enumerate(menu_options):
            color = white if i != selected_option else green
            draw_text(screen, option, 36, screen_width // 2, screen_height // 2 - 50 + i * 50, color=color, align="center")

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

def show_rules(screen):
    try:
        with open(help_file, "r", encoding="utf-8") as f:
            rules = f.read().split('\n')
    except FileNotFoundError:
        rules = ["Arquivo de ajuda não encontrado."]
    
    screen.fill(black)
    y_offset = 100
    for line in rules:
        draw_text(screen, line, 24, screen_width // 2, y_offset, align="center", max_width=screen_width - 40)
        y_offset += 30

    draw_text(screen, "Pressione Enter para voltar ao menu", 24, screen_width // 2, screen_height - 50, align="center")
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        pygame.time.Clock().tick(30)

def show_high_scores(screen):
    high_scores = load_high_scores()
    screen.fill(black)
    draw_text(screen, "Melhores Pontuações", 48, screen_width // 2, 50, align="center")

    y_offset = 150
    for score, date in high_scores:
        draw_text(screen, f"{score} - {date}", 36, screen_width // 2, y_offset, align="center")
        y_offset += 40

    draw_text(screen, "Pressione Enter para voltar ao menu", 24, screen_width // 2, screen_height - 50, align="center")
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        pygame.time.Clock().tick(30)

def move_objects(objects, speeds, directions):
    for i, obj in enumerate(objects):
        if isinstance(obj, dict):
            obj_rect = obj["rect"]
        else:
            obj_rect = obj
        
        # Atualiza a posição com base na velocidade e direção
        obj_rect.x += speeds[i] * directions[i].x
        obj_rect.y += speeds[i] * directions[i].y
        
        # Altera a direção se atingir as bordas
        if obj_rect.left < 0 or obj_rect.right > screen_width:
            directions[i].x *= -1
        if obj_rect.top < 100 or obj_rect.bottom > screen_height - 100:
            directions[i].y *= -1
        
        # Verifica colisão com outros objetos
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

def update_powerups(player, obstacles, obstacle_speeds):
    global active_powerups
    current_time = time.time()
    for powerup in active_powerups[:]:
        remaining_time = POWERUP_DURATION - (current_time - powerup["start_time"])
        if remaining_time <= 0:
            if powerup["type"] == "speed":
                player.speed = PLAYER_BASE_SPEED
            elif powerup["type"] == "collect":
                player.radius //= 2
            elif powerup["type"] == "slow":
                for i in range(len(obstacle_speeds)):
                    obstacle_speeds[i] *= 100  # Restaura a velocidade original dos obstáculos
            active_powerups.remove(powerup)
        else:
            draw_text(screen, f"{int(remaining_time)}s", 24, screen_width - 60, 20 + 50 * active_powerups.index(powerup), align="right")
            if powerup.get("hourglass_image"):
                screen.blit(powerup["hourglass_image"], (screen_width - 50, 10 + 50 * active_powerups.index(powerup)))



