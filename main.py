# main.py
import pygame
import time
from config import *
from level import *
from powerups import *
from ui import *
from audio import *
from utils import *
from questions import QuestionManager
from player import Player
from graphics import draw_objects

def initialize_game():
    
    pygame.mouse.set_visible(False)
    
    global player, player_health, level_num, items, obstacles
    global item_speeds, obstacle_speeds, item_directions, obstacle_directions
    global powerups, powerup_speeds, powerup_directions
    global message, score, current_question, high_scores
    global collision_count, correct_answers, correct_answers_streak
    global player_radius, game_start_time, start_time, last_item_collect_time, answered_questions, active_powerups, running
    global question_manager, powerup_manager, question_file, current_question, addition_obstacles_for_wrong_answer

    INITIAL_VALUES = {
        "last_item_collect_time": INITIAL_LAST_ITEM_COLLECT_TIME,
        "collision_count": INITIAL_COLLISION_COUNT,
        "player_health": INITIAL_HEALTH,
        "score": INITIAL_SCORE,
        "level_num": INITIAL_LEVEL,
        "correct_answers": INITIAL_CORRECT_ANSWERS,
        "correct_answers_streak": INITIAL_CORRECT_ANSWERS_STREAK,
        "question_file": question_file
    }
    for var, value in INITIAL_VALUES.items():
        globals()[var] = value

    # Carregar os melhores scores
    high_scores = load_high_scores()

    # Inicializa o Gerenciador de Questões e carrega as questões
    question_manager = QuestionManager(question_file)
    question_manager.load_questions()
    answered_questions = set()
    current_question = None

    # Inicializar jogador, obstáculos, itens, etc.
    player = Player()
    powerup_manager = PowerUpManager()
    items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions, powerups, powerup_speeds, powerup_directions, message = create_level(INITIAL_LEVEL, powerup_manager)

    # Inicializa o estado do jogo
    game_start_time = 0
    start_time = 0

def handle_events():
    global running, current_question, correct_answers, correct_answers_streak, score, collision_count
    global items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions, powerups
    global powerup_speeds, powerup_directions, player

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                show_pause_menu(screen)
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                if current_question:
                    selected_option = int(event.unicode)
                    is_correct = question_manager.check_answer(current_question, selected_option)
                    if is_correct:
                        correct_answers += 1
                        correct_answers_streak += 1
                        score += POINTS_FOR_CORRECT_ANSWER
                        question_manager.mark_question_as_answered(current_question)
                        current_question = None
                    else:
                        play_sound(errou_sound_path)
                        score -= POINTS_FOR_CORRECT_ANSWER
                        current_question = None
                        correct_answers_streak = 0
                        for _ in range(addition_obstacles_for_wrong_answer):
                            obstacles, obstacle_speeds, obstacle_directions = create_obstacle(obstacles, obstacle_speeds, obstacle_directions, level_num)

def update_game_state():
    global items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions
    global powerups, powerup_speeds, powerup_directions, player, current_question, score
    global start_time, collision_count, running, level_num

    player.move()

    # Verifica colisão com itens
    for item in items[:]:
        if player.rect.colliderect(item):
            play_sound(item_collect_sound_path)
            index = items.index(item)
            items.remove(item)
            item_speeds.pop(index)
            item_directions.pop(index)
            last_item_collect_time = time.time()
            current_question = question_manager.get_random_question()
            score += 1

    # Verifica colisão com obstáculos
    for obstacle in obstacles[:]:
        if player.rect.colliderect(obstacle):
            if player.shield_active:
                obstacles.remove(obstacle)
                play_sound(obstacle_destroyed_sound_path)
            else:
                play_sound(obstacle_collision_sound_path)
                collision_count += 1
                index = obstacles.index(obstacle)
                obstacles.remove(obstacle)
                obstacle_speeds.pop(index)
                obstacle_directions.pop(index)
                player.health -= 1
                if player.health <= 0:
                    running = False
                    show_game_over_screen(screen, score, collision_count, level_num, correct_answers, correct_answers_streak, high_scores)
                    main()

    # Verifica colisão com power-ups
    for powerup in powerups[:]:
        if player.rect.colliderect(powerup["rect"]):
            play_sound(powerup_manager.powerup_types[powerup["type"]]["sound"])
            powerup_manager.apply_powerup_effect(powerup["type"], player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions)
            powerup_speeds.pop(powerups.index(powerup))
            powerup_directions.pop(powerups.index(powerup))
            powerups.remove(powerup)

    # Movimento dos power-ups
    powerups, powerup_speeds, powerup_directions = move_objects(powerups, powerup_speeds, powerup_directions)

    # Atualiza os efeitos dos power-ups e exibe a contagem regressiva
    powerup_manager.update_powerups(player, items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions)

    # Verifica se o nível foi concluído
    if not items:
        level_num += 1
        items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions, powerups, powerup_speeds, powerup_directions, message = create_level(level_num, powerup_manager)
        player.rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        play_sound(level_up_sound_path)

    # Movimento dos itens e obstáculos
    items, item_speeds, item_directions = move_objects(items, item_speeds, item_directions)
    obstacles, obstacle_speeds, obstacle_directions = move_objects(obstacles, obstacle_speeds, obstacle_directions)

    # Função para calcular novas velocidades após colisão
    def handle_collision(obj1, obj2, direction1, direction2, speed1, speed2, mass1, mass2):
        new_speed1 = ((mass1 - mass2) / (mass1 + mass2)) * speed1 + ((2 * mass2) / (mass1 + mass2)) * speed2
        new_speed2 = ((2 * mass1) / (mass1 + mass2)) * speed1 + ((mass2 - mass1) / (mass1 + mass2)) * speed2
        direction1.reflect_ip(direction2)
        direction2.reflect_ip(direction1)
        return new_speed1, new_speed2

    # Colisões entre itens e obstáculos
    for i, item in enumerate(items):
        for j, obstacle in enumerate(obstacles):
            if item.colliderect(obstacle):
                new_item_speed, new_obstacle_speed = handle_collision(
                    item, obstacle,
                    item_directions[i], obstacle_directions[j],
                    item_speeds[i], obstacle_speeds[j],
                    MASS_ITEM, MASS_OBSTACLE
                )
                item_speeds[i] = new_item_speed
                obstacle_speeds[j] = new_obstacle_speed

    # Colisões entre itens e itens
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i].colliderect(items[j]):
                new_speed1, new_speed2 = handle_collision(
                    items[i], items[j],
                    item_directions[i], item_directions[j],
                    item_speeds[i], item_speeds[j],
                    MASS_ITEM, MASS_ITEM
                )
                item_speeds[i] = new_speed1
                item_speeds[j] = new_speed2

    # Colisões entre obstáculos e obstáculos
    for i in range(len(obstacles)):
        for j in range(i + 1, len(obstacles)):
            if obstacles[i].colliderect(obstacles[j]):
                new_speed1, new_speed2 = handle_collision(
                    obstacles[i], obstacles[j],
                    obstacle_directions[i], obstacle_directions[j],
                    obstacle_speeds[i], obstacle_speeds[j],
                    MASS_OBSTACLE, MASS_OBSTACLE
                )
                obstacle_speeds[i] = new_speed1
                obstacle_speeds[j] = new_speed2

    # Colisões entre power-ups e obstáculos
    for powerup in powerups:
        for obstacle in obstacles:
            if powerup["rect"].colliderect(obstacle):
                new_powerup_speed, new_obstacle_speed = handle_collision(
                    powerup["rect"], obstacle,
                    powerup_directions[powerups.index(powerup)], obstacle_directions[obstacles.index(obstacle)],
                    powerup_speeds[powerups.index(powerup)], obstacle_speeds[obstacles.index(obstacle)],
                    MASS_POWERUP, MASS_OBSTACLE
                )
                powerup_speeds[powerups.index(powerup)] = new_powerup_speed
                obstacle_speeds[obstacles.index(obstacle)] = new_obstacle_speed

    # Colisões entre power-ups e itens
    for powerup in powerups:
        for item in items:
            if powerup["rect"].colliderect(item):
                new_powerup_speed, new_item_speed = handle_collision(
                    powerup["rect"], item,
                    powerup_directions[powerups.index(powerup)], item_directions[items.index(item)],
                    powerup_speeds[powerups.index(powerup)], item_speeds[items.index(item)],
                    MASS_POWERUP, MASS_ITEM
                )
                powerup_speeds[powerups.index(powerup)] = new_powerup_speed
                item_speeds[items.index(item)] = new_item_speed

    # Colisões entre power-ups e power-ups
    for i in range(len(powerups)):
        for j in range(i + 1, len(powerups)):
            if powerups[i]["rect"].colliderect(powerups[j]["rect"]):
                new_speed1, new_speed2 = handle_collision(
                    powerups[i]["rect"], powerups[j]["rect"],
                    powerup_directions[i], powerup_directions[j],
                    powerup_speeds[i], powerup_speeds[j],
                    MASS_POWERUP, MASS_POWERUP
                )
                powerup_speeds[i] = new_speed1
                powerup_speeds[j] = new_speed2

    # Cronômetro para subtrair pontos do score a cada intervalo de tempo
    if time.time() - start_time > score_decrement_interval:
        score -= 1
        start_time = time.time()

def render():
    global score, player, items, obstacles, powerups
    global correct_answers_streak, level_num, collision_count, current_question

    screen.fill(black)

    draw_objects(screen, items, obstacles)
    player.draw(screen)  # Desenha o jogador
    powerup_manager.draw_powerups(screen, powerups)  # Passa a lista de powerups para o método
    powerup_manager.draw_active_powerups(screen)

    draw_text(screen, f"Score: {score}", 24, 10, 10, color=white, align="left")
    draw_text(screen, f"Vidas: {player.health}", 24, 10, 40, color=white, align="left")
    draw_text(screen, f"Nível: {level_num}", 24, 10, 70, color=white, align="left")
    draw_text(screen, f"Colisões: {collision_count}", 24, 10, 100, color=white, align="left")

    remaining_questions = question_manager.get_remaining_questions_count()
    if remaining_questions>0:
        draw_text(screen, f"Perguntas Restantes: {remaining_questions}", 24, 10, 130, color=white, align="left")
    else:
        pygame.mixer.music.stop()
        play_sound(congratulations_sound_file)
        show_congratulations_screen(screen,congratulations_image_file)
        save_high_scores(score, high_scores)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                show_main_menu(screen)
        
    if current_question:
        draw_text(screen, current_question["pergunta"], 24, SCREEN_WIDTH // 2, 10, color=white, align="center")
        for i in range(1, 5):
            draw_text(screen, f"{i}. {current_question[f'opcao_{i}']}", 24, SCREEN_WIDTH // 2, 40 + i * 30, color=white, align="center")

    pygame.display.flip()

def main():
    global running
    initialize_game()
    show_main_menu(screen)
    show_start_screen(screen)

    running = True
    clock = pygame.time.Clock()

    while running:
        handle_events()
        update_game_state()
        render()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.mouse.set_visible(True)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    main()
    pygame.quit()