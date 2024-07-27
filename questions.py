# questions.py
import random
import pandas as pd
from config import *
from utils import draw_text

# questions.py
class QuestionManager:
    def __init__(self, question_file):
        self.question_file = question_file
        self.questions = self.load_questions()
        self.answered_questions = set()

    def load_questions(self):
        try:
            df = pd.read_excel(self.question_file)
            return df.to_dict(orient="records")
        except FileNotFoundError:
            return [
                {"pergunta": "Qual é o maior mandamento?", "opcao_1": "Amar a Deus sobre todas as coisas", "opcao_2": "Não matar", "opcao_3": "Guardar o sábado", "opcao_4": "Não roubar", "resposta": "1"}
            ]

    def get_random_question(self):
        available_questions = [q for q in self.questions if q["pergunta"] not in self.answered_questions]
        if not available_questions:
            return None
        question = random.choice(available_questions)
        return question

    def check_answer(self, question, answer):
        correct_answer = str(question["resposta"]).strip()
        received_answer = str(answer).strip()
        return correct_answer == received_answer

    def mark_question_as_answered(self, question):
        self.answered_questions.add(question["pergunta"])

    def show_question(self, screen, question, selected_option=None, is_correct=None):
        option_colors = [white, white, white, white]
        if selected_option is not None:
            if is_correct:
                option_colors[selected_option - 1] = green
            else:
                option_colors[selected_option - 1] = red
        draw_text(screen, question["pergunta"], 24, screen_width // 2, 70, color=white, align="center", max_width=screen_width - 40)
        draw_text(screen, f"1. {question['opcao_1']}", 24, screen_width // 2, 110, color=option_colors[0], align="center", max_width=screen_width - 40)
        draw_text(screen, f"2. {question['opcao_2']}", 24, screen_width // 2, 150, color=option_colors[1], align="center", max_width=screen_width - 40)
        draw_text(screen, f"3. {question['opcao_3']}", 24, screen_width // 2, 190, color=option_colors[2], align="center", max_width=screen_width - 40)
        draw_text(screen, f"4. {question['opcao_4']}", 24, screen_width // 2, 230, color=option_colors[3], align="center", max_width=screen_width - 40)



# import random
# import pandas as pd
# from config import *
# from utils import draw_text

# class QuestionManager:
#     def __init__(self, question_file):
#         self.question_file = question_file
#         self.questions = self.load_questions()
#         self.answered_questions = set()
#         self.current_question = None

#     def load_questions(self):
#         try:
#             df = pd.read_excel(self.question_file)
#             return df.to_dict(orient="records")
#         except FileNotFoundError:
#             return [
#                 {"pergunta": "Qual é o maior mandamento?", "opcao_1": "Amar a Deus sobre todas as coisas", "opcao_2": "Não matar", "opcao_3": "Guardar o sábado", "opcao_4": "Não roubar", "resposta": "1"}
#             ]

#     def get_random_question(self):
#         available_questions = [q for q in self.questions if q["pergunta"] not in self.answered_questions]
#         if not available_questions:
#             return None
#         self.current_question = random.choice(available_questions)
#         return self.current_question

#     def check_answer(self, answer):
#         if not self.current_question:
#             return False
#         correct_answer = str(self.current_question["resposta"]).strip()
#         received_answer = str(answer).strip()
#         return correct_answer == received_answer

#     def mark_question_as_answered(self):
#         if self.current_question:
#             self.answered_questions.add(self.current_question["pergunta"])

#     def show_question(self, screen, selected_option=None, is_correct=None):
#         if not self.current_question:
#             return
#         option_colors = [white, white, white, white]
#         if selected_option is not None:
#             if is_correct:
#                 option_colors[selected_option - 1] = green
#             else:
#                 option_colors[selected_option - 1] = red
#         draw_text(screen, self.current_question["pergunta"], 24, screen_width // 2, 70, align="center", max_width=screen_width - 40)
#         draw_text(screen, f"1. {self.current_question['opcao_1']}", 24, screen_width // 2, 110, color=option_colors[0], align="center", max_width=screen_width - 40)
#         draw_text(screen, f"2. {self.current_question['opcao_2']}", 24, screen_width // 2, 150, color=option_colors[1], align="center", max_width=screen_width - 40)
#         draw_text(screen, f"3. {self.current_question['opcao_3']}", 24, screen_width // 2, 190, color=option_colors[2], align="center", max_width=screen_width - 40)
#         draw_text(screen, f"4. {self.current_question['opcao_4']}", 24, screen_width // 2, 230, color=option_colors[3], align="center", max_width=screen_width - 40)

#     def reset(self):
#         self.answered_questions = set()
#         self.current_question = None



# # questions.py
# import random
# import pandas as pd
# from config import *
# from utils import draw_text

# def load_questions():
#     try:
#         df = pd.read_excel(question_file)
#         return df.to_dict(orient="records")
#     except FileNotFoundError:
#         return [
#             {"pergunta": "Qual é o maior mandamento?", "opcao_1": "Amar a Deus sobre todas as coisas", "opcao_2": "Não matar", "opcao_3": "Guardar o sábado", "opcao_4": "Não roubar", "resposta": "1"}
#         ]

# def get_random_question(questions, answered_questions):
#     available_questions = [q for q in questions if q["pergunta"] not in answered_questions]
#     if not available_questions:
#         return None
#     question = random.choice(available_questions)
#     return question

# def check_answer(question, answer):
#     correct_answer = str(question["resposta"]).strip()
#     received_answer = str(answer).strip()
#     return correct_answer == received_answer

# def show_question(screen, question, selected_option=None, is_correct=None):
#     option_colors = [white, white, white, white]
#     if selected_option is not None:
#         if is_correct:
#             option_colors[selected_option - 1] = green
#         else:
#             option_colors[selected_option - 1] = red
#     draw_text(screen, question["pergunta"], 24, screen_width // 2, 70, align="center", max_width=screen_width - 40)
#     draw_text(screen, f"1. {question['opcao_1']}", 24, screen_width // 2, 110, color=option_colors[0], align="center", max_width=screen_width - 40)
#     draw_text(screen, f"2. {question['opcao_2']}", 24, screen_width // 2, 150, color=option_colors[1], align="center", max_width=screen_width - 40)
#     draw_text(screen, f"3. {question['opcao_3']}", 24, screen_width // 2, 190, color=option_colors[2], align="center", max_width=screen_width - 40)
#     draw_text(screen, f"4. {question['opcao_4']}", 24, screen_width // 2, 230, color=option_colors[3], align="center", max_width=screen_width - 40)