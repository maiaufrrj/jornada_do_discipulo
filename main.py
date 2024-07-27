import pygame
import random
import time
import pandas as pd
from config import *
from utils import *
from player import *
from powerups import *
from level import *
from questions import QuestionManager

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("A Jornada do Discípulo")

# Carregar sons
pygame.mixer.init()
acertou = pygame.mixer.Sound(acertou_sound_path)
errou = pygame.mixer.Sound(errou_sound_path)
obstacle_collision = pygame.mixer.Sound(obstacle_collision_sound_path)
item_collect = pygame.mixer.Sound(item_collect_sound_path)
game_over_music = pygame.mixer.Sound(game_over_sound_path)
zerou_sound = pygame.mixer.Sound(zerou_sound_path)
level_up_sound = pygame.mixer.Sound(level_up_sound_path)

# Carregar a imagem de parabéns
congratulations_image = pygame.image.load(congratulations_image_file)
congratulations_image = pygame.transform.scale(congratulations_image, (screen_width, screen_height))

def main():
    pygame.init()
    global player, player_health, level_num, items, obstacles
    global item_speeds, obstacle_speeds, item_directions, obstacle_directions
    global health_items, powerups, powerup_speeds, powerup_directions
    global message, score, health_spawn_time, current_question, high_scores
    global collision_count, correct_answers, correct_answers_streak
    global player_radius, player_velocity, game_start_time, start_time
    global last_item_collect_time, answered_questions, active_powerups, running
    global question_manager, question_file, current_question, running

    # Constantes de inicialização
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
    
    # Inicializa variáveis globais com valores iniciais
    for var, value in INITIAL_VALUES.items():
        globals()[var] = value

    current_question = None
    game_start_time = 0
    
    # Mostrar menu principal
    show_main_menu(screen)

    # Inicializa o Gerenciador de Questões e carrega as questões
    question_manager = QuestionManager(question_file)

    # Inicializar jogador, obstáculos, itens, etc.
    player = Player()
    powerup_manager = PowerUpManager()

    items, item_speeds, item_directions, obstacles, obstacle_speeds, obstacle_directions, health_items, powerups, powerup_speeds, powerup_directions, message = create_level(INITIAL_LEVEL, powerup_manager)

    #powerup_manager.update_powerups(player, obstacles, obstacle_speeds, obstacle_directions)

    # Inicializa o estado do jogo
    running = True
    health_spawn_time = time.time()
    start_time = time.time()
    game_start_time = time.time()

    # Mostrar tela de início
    show_start_screen(screen)

    clock = pygame.time.Clock()


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    pause_action = show_pause_menu(screen)
                    if pause_action == "restart":
                        main()
                        return
                if current_question:
                    if event.key == pygame.K_1:
                        answer = "1"
                    elif event.key == pygame.K_2:
                        answer = "2"
                    elif event.key == pygame.K_3:
                        answer = "3"
                    elif event.key == pygame.K_4:
                        answer = "4"
                    else:
                        answer = None

                    if answer:
                        if question_manager.check_answer(current_question, answer):
                            score += 3
                            correct_answers += 1
                            correct_answers_streak += 1
                            answered_questions.add(current_question["pergunta"])
                            print(f"Resposta correta! Streak: {correct_answers_streak}, Total corretas: {correct_answers}")  # Mensagem de depuração
                            question_manager.show_question(screen, current_question, int(answer), True)
                            play_sound(acertou_sound_path)
                            obstacles_to_remove = 1
                            if level_num > 5:
                                obstacles_to_remove = 2
                            if level_num > 8:
                                obstacles_to_remove = 3
                            if obstacles:
                                for _ in range(min(obstacles_to_remove, len(obstacles))):
                                    idx = random.randint(0, len(obstacles) - 1)
                                    obstacles.pop(idx)
                                    obstacle_speeds.pop(idx)
                                    obstacle_directions.pop(idx)
                            if correct_answers_streak >= 3:
                                player.health += 1
                                correct_answers_streak = 0  # Reinicia a contagem de respostas corretas
                            current_question = None
                            if len(answered_questions) == len(question_manager.questions):
                                show_congratulations_screen(screen, load_image(congratulations_image_file), play_sound(zerou_sound_path))
                                running = False
                        else:
                            correct_answers_streak = 0  # Reinicia a contagem de respostas corretas
                            score -= 1
                            print("Resposta incorreta.")  # Mensagem de depuração
                            question_manager.show_question(screen, current_question, int(answer), False)
                            play_sound(errou_sound_path)
                            for _ in range(3):
                                create_obstacle(obstacles, obstacle_speeds, obstacle_directions, level_num)
                            current_question = None

        # Movimento do jogador
        move_player(player.rect, player.speed, game_start_time)

        # Verifica colisão com itens
        for item in items[:]:
            if player.rect.colliderect(item):
                items.remove(item)
                score += 1
                play_sound(item_collect_sound_path)
                print(f"Coletou item. Pontos: {score}")  # Mensagem de depuração
                last_item_collect_time = time.time()
                current_question = question_manager.get_random_question()
                if not current_question:
                    show_congratulations_screen(screen, load_image(congratulations_image_file), play_sound(zerou_sound_path))
                    running = False
                    break
                print(f"Nova pergunta: {current_question['pergunta']}")  # Mensagem de depuração

        # Verifica colisão com obstáculos
        for obstacle in obstacles[:]:
            if player.rect.colliderect(obstacle):
                player.health -= 1
                collision_count += 1
                idx = obstacles.index(obstacle)
                obstacles.remove(obstacle)
                obstacle_speeds.pop(idx)
                obstacle_directions.pop(idx)
                play_sound(obstacle_collision_sound_path)
                print(f"Colidiu com obstáculo. Vidas restantes: {player.health}")  # Mensagem de depuração
                if player.health <= 0 or score <= 0:
                    running = False
                    message = "Game Over"
                    print(message)  # Mensagem de depuração

        # Verifica colisão com itens de saúde
        for health_item in health_items[:]:
            if player.rect.colliderect(health_item):
                health_items.remove(health_item)
                player.health += 1

        # Verificar colisão com power-ups
        for powerup in powerup_manager.active_powerups:
            if player.rect.colliderect(powerup["rect"]):
                powerup_manager.apply_powerup_effect(powerup, player, obstacles, obstacle_speeds, obstacle_directions)


        # Movimento dos power-ups
        powerups, powerup_speeds, powerup_directions = move_objects(powerups, powerup_speeds, powerup_directions)

        # Atualiza os efeitos dos power-ups e exibe a contagem regressiva
        update_powerups(player, obstacles, obstacle_speeds)
        draw_active_powerups(screen)

        # Verifica se o nível foi concluído
        if not items:
            level_num += 1
            # Reinicia qualquer efeito de power-ups, incluindo ampulheta e contagem de tempo de efeito
            active_powerups = []
            items, obstacles, item_speeds, obstacle_speeds, item_directions, obstacle_directions, health_items, powerups, powerup_speeds, powerup_directions, message = create_level(level_num)
            player.radius += 2  # Aumenta o raio do jogador a cada nível
            player.rect = pygame.Rect(player.rect.x, player.rect.y, player.radius * 2, player.radius * 2)
            player.speed = PLAYER_BASE_SPEED + level_num * PLAYER_SPEED_INCREMENT  # Incrementa a velocidade do jogador com o nível
            play_sound(level_up_sound_path)
            print(f"Iniciando nível {level_num}")  # Mensagem de depuração

        # Movimento dos itens e obstáculos
        items, item_speeds, item_directions = move_objects(items, item_speeds, item_directions)
        obstacles, obstacle_speeds, obstacle_directions = move_objects(obstacles, obstacle_speeds, obstacle_directions)

        # Aparição aleatória de itens de saúde
        if level_num > 5 and time.time() - health_spawn_time > random.randint(10, 20):
            health_items = [pygame.Rect(random.randint(0, screen_width - 20), random.randint(100, screen_height - 120), 20, 20)]
            health_spawn_time = time.time()

        # Remover itens de saúde após 5 segundos
        if health_items and time.time() - health_spawn_time > 5:
            health_items = []

        # Cronômetro para subtrair pontos do score a cada intervalo de tempo
        current_time = time.time()
        if current_time - last_item_collect_time >= score_decrement_interval:
            if score > 0:  # Apenas decrementar se o score for maior que 0
                score -= 1
            last_item_collect_time = current_time  # Reseta o tempo
            print(f"Score atualizado: {score}")  # Mensagem de depuração
            if score <= 0:
                running = False
                message = "Game Over"
                print(message)  # Mensagem de depuração

        # Desenha na tela
        screen.fill(black)
        pygame.draw.circle(screen, green, player.rect.center, player.radius)
        for item in items:
            pygame.draw.rect(screen, white, item)
        for obstacle in obstacles:
            pygame.draw.rect(screen, red, obstacle)
        for health_item in health_items:
            pygame.draw.rect(screen, yellow, health_item)

        # Desenhar power-ups
        for powerup in powerups:
            powerup_image = powerup_images.get(powerup["type"])
            if powerup_image:
                # Centraliza a imagem no centro do retângulo
                image_rect = powerup_image.get_rect(center=powerup["rect"].center)
                screen.blit(powerup_image, image_rect.topleft)
            else:
                # Não desenha mais o retângulo se a imagem não for carregada
                print(f"Image not found for powerup: {powerup['type']}")

        # Exibe a pontuação, número de vidas, nível atual e contagem de colisões
        draw_text(screen, f"Pontos: {score}", 24, 10, 10, align="left")
        draw_text(screen, f"Vidas: {player.health}", 24, 10, 40, align="left")
        draw_text(screen, f"Nível: {level_num}", 24, 10, 70, align="left")
        draw_text(screen, f"Colisões: {collision_count}", 24, 10, 100, align="left")

        # Exibe a pergunta na parte superior da tela
        if current_question:
            question_manager.show_question(screen, current_question)

        pygame.display.flip()
        clock.tick(30)

    # Atualiza os melhores scores
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")
    high_scores.append([str(score), date_str])
    high_scores = sorted(high_scores, key=lambda x: int(x[0]), reverse=True)[:10]
    save_high_scores(high_scores)

    # Exibe a tela de Game Over com os resultados
    pygame.mixer.stop()  # Para qualquer música ou som em andamento
    play_sound(game_over_sound_path)

    duration_seconds = int(time.time() - game_start_time)
    duration_minutes = duration_seconds // 60
    duration_seconds = duration_seconds % 60
    duration_formatted = f"{duration_minutes:02}:{duration_seconds:02}"

    screen.fill(black)
    draw_text(screen, "Game Over", 48, screen_width // 2, screen_height // 2 - 100, align="center")
    draw_text(screen, f"Pontuação Final: {score}", 36, screen_width // 2, screen_height // 2 - 50, align="center")
    draw_text(screen, f"Nível Final: {level_num}", 36, screen_width // 2, screen_height // 2, align="center")
    draw_text(screen, f"Duração da Partida: {duration_formatted}", 36, screen_width // 2, screen_height // 2 + 50, align="center")
    draw_text(screen, f"Respostas Corretas: {correct_answers}", 36, screen_width // 2, screen_height // 2 + 100, align="center")
    draw_text(screen, f"Colisões: {collision_count}", 36, screen_width // 2, screen_height // 2 + 150, align="center")
    pygame.display.flip()

    # Aguarda TIME_TO_START segundos antes de permitir entrada do usuário
    time.sleep(TIME_TO_START)

    # Aguarda entrada do usuário para voltar ao menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                reset_game()
                main()  # Reinicia o jogo
                return
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()
