# utils.py
import pygame
import time
import random
import pandas as pd
from config import *
from level import *

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
        if obj_rect.left < 0 or obj_rect.right > SCREEN_WIDTH:
            directions[i].x *= -1
        if obj_rect.top < 100 or obj_rect.bottom > SCREEN_HEIGHT - 100:
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

def play_sound(sound_path):
    if sound_path:  # Verificar se sound_path não é None
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
        except pygame.error as e:
            print(f"Warning: Could not play sound: {sound_path}. {e}")
    else:
        print("Warning: No sound path provided")

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

def save_high_scores(score, scores):
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")
    scores.append([str(score), date_str])
    scores = sorted(scores, key=lambda x: int(x[0]), reverse=True)
    with open(score_file, "w", encoding="utf-8") as f:
        for score, date in scores:
            f.write(f"{score},{date}\n")

# def save_high_scores(scores):
#     with open(score_file, "w", encoding="utf-8") as f:
#         for score, date in scores:
#             f.write(f"{score},{date}\n")

# def load_questions():
#     try:
#         df = pd.read_excel(question_file)
#         return df.to_dict(orient="records")
#     except FileNotFoundError:
#         return [
#             {"pergunta": "Qual é o maior mandamento?", "opcao_1": "Amar a Deus sobre todas as coisas", "opcao_2": "Não matar", "opcao_3": "Guardar o sábado", "opcao_4": "Não roubar", "resposta": "1"}
#         ]

# def show_question(screen, question, selected_option=None, is_correct=None):
#     option_colors = [white, white, white, white]
#     if selected_option is not None:
#         if is_correct:
#             option_colors[selected_option - 1] = green
#         else:
#             option_colors[selected_option - 1] = red
#     draw_text(screen, question["pergunta"], 24, SCREEN_WIDTH // 2, 70, align="center", max_width=SCREEN_WIDTH - 40)
#     draw_text(screen, f"1. {question['opcao_1']}", 24, SCREEN_WIDTH // 2, 110, color=option_colors[0], align="center", max_width=SCREEN_WIDTH - 40)
#     draw_text(screen, f"2. {question['opcao_2']}", 24, SCREEN_WIDTH // 2, 150, color=option_colors[1], align="center", max_width=SCREEN_WIDTH - 40)
#     draw_text(screen, f"3. {question['opcao_3']}", 24, SCREEN_WIDTH // 2, 190, color=option_colors[2], align="center", max_width=SCREEN_WIDTH - 40)
#     draw_text(screen, f"4. {question['opcao_4']}", 24, SCREEN_WIDTH // 2, 230, color=option_colors[3], align="center", max_width=SCREEN_WIDTH - 40)

# def check_answer(question, answer):
#     correct_answer = str(question["resposta"]).strip()
#     received_answer = str(answer).strip()
#     return correct_answer == received_answer

# def get_random_question(questions, answered_questions):
#     available_questions = [q for q in questions if q["pergunta"] not in answered_questions]
#     if not available_questions:
#         return None
#     question = random.choice(available_questions)
#     return question

# def show_start_screen(screen):
#     start_time = time.time()
#     countdown = TIME_TO_START
#     while True:
#         screen.fill(black)
#         current_time = time.time()
#         elapsed_time = current_time - start_time
#         remaining_time = max(0, countdown - int(elapsed_time))
        
#         if remaining_time == 0:
#             break

#         draw_text(screen, f"Preparando para começar! ({remaining_time})", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, color=white, align="center")

#         pygame.display.flip()
#         pygame.time.Clock().tick(30)



