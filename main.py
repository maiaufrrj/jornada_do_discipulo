import pygame
import time
import random
from config import *
from level import *
from powerups import *
from ui import *
from audio import *
from utils import *
from questions import QuestionManager
from player import Player
from graphics import draw_objects


# Inicializa o Pygame
pygame.init()

# Carrega sons
item_collect_sound = pygame.mixer.Sound(item_collect_sound_path)

def main():
    global player, player_health, level_num, items, obstacles
    global item_speeds, obstacle_speeds, item_directions, obstacle_directions
    global health_items, powerups, powerup_speeds, powerup_directions
    global message, score, health_spawn_time, current_question, high_scores
    global collision_count, correct_answers, correct_answers_streak
    global player_radius, player_velocity, game_start_time, start_time
    global last_item_collect_time, answered_questions, active_powerups, running
    global question_manager, powerup_manager, question_file, current_question

    # Inicializa variáveis globais com valores iniciais
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

    # Mostrar menu principal
    show_main_menu(screen)

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
    items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions, health_items, powerups, powerup_speeds, powerup_directions, message = create_level(INITIAL_LEVEL, powerup_manager)

    # Inicializa o estado do jogo
    game_start_time = 0
    start_time = 0
    health_spawn_time = time.time()

    # Mostrar tela de início
    show_start_screen(screen)

    running = True
    clock = pygame.time.Clock()

    # Loop principal
    while running:
        screen.fill(black)

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
                            correct_answers_streak = 0
                            player.health -= 1
        
        keys = pygame.key.get_pressed()
        player.move(keys)

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
                play_sound(obstacle_collision_sound_path)
                collision_count += 1
                index = obstacles.index(obstacle)
                obstacles.remove(obstacle)
                obstacle_speeds.pop(index)
                obstacle_directions.pop(index)
                player.health -= 1
                if player.health <= 0:
                    show_game_over_screen(screen, score, collision_count, level_num, correct_answers, correct_answers_streak, high_scores)
                    running = False

        # Verifica colisão com itens de saúde
        for health_item in health_items[:]:
            if player.rect.colliderect(health_item):
                player.health += 1
                health_items.remove(health_item)
            
        # Verifica colisão com power-ups
        for powerup in powerups[:]:
            if player.rect.colliderect(powerup["rect"]):
                play_sound(powerup_manager.powerup_types[powerup["type"]]["sound"])
                powerup_manager.apply_powerup_effect(powerup["type"], player, obstacles, obstacle_speeds, obstacle_directions)
                powerups.remove(powerup)

        # Atualiza os efeitos dos power-ups e exibe a contagem regressiva
        powerup_manager.update_powerups(player, obstacles, obstacle_speeds, obstacle_directions)

        # Movimento dos itens e obstáculos
        items, item_speeds, item_directions = move_objects(items, item_speeds, item_directions)
        obstacles, obstacle_speeds, obstacle_directions = move_objects(obstacles, obstacle_speeds, obstacle_directions)

        # Aparição aleatória de itens de saúde
        if time.time() - health_spawn_time >= 5:
            health_spawn_time = time.time()
            health_item_rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), random.randint(100, SCREEN_HEIGHT - 120), 20, 20)
            health_items.append(health_item_rect)

        # Remover itens de saúde após 5 segundos
        health_items = [item for item in health_items if time.time() - health_spawn_time < 5]

        # Cronômetro para subtrair pontos do score a cada intervalo de tempo
        current_time = time.time()
        if current_time - last_item_collect_time >= score_decrement_interval:
            score -= 1
            last_item_collect_time = current_time

        ## Desenha na tela
        screen.fill(black)
        
        # Desenha jogador
        player.draw(screen) 

        draw_objects(screen, items, obstacles, health_items, powerups)
        powerup_manager.draw_powerups(screen)
        
        # Exibe a pontuação, número de vidas, nível atual e contagem de colisões
        draw_text(screen, f"Score: {score}", 24, 10, 10, color=white, align="left")
        draw_text(screen, f"Vidas: {player.health}", 24, 10, 40, color=white, align="left")
        draw_text(screen, f"Nível: {level_num}", 24, 10, 70, color=white, align="left")
        draw_text(screen, f"Colisões: {collision_count}", 24, 10, 100, color=white, align="left")

        # Exibe a pergunta na parte superior da tela
        if current_question:
            question_manager.show_question(screen, current_question)

        pygame.display.flip()
        clock.tick(30)

    # Para qualquer música ou som em andamento
    pygame.mixer.music.stop()

    # Exibe a tela de Game Over com os resultados
    show_game_over_screen(screen, score, collision_count, level_num, correct_answers, correct_answers_streak, high_scores)

    # Aguarda TIME_TO_START segundos antes de permitir entrada do usuário
    pygame.time.wait(TIME_TO_START * 1000)

    # Aguarda entrada do usuário para voltar ao menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_main_menu(screen)
                    return

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    main()
    pygame.quit()


