import pygame

# Configurações da tela
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen_width, screen_height = screen.get_size()
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("A Jornada do Discípulo")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
cyan = (0, 255, 255)
orange = (255, 165, 0)
pink = (255, 192, 203)
yellow = (255, 255, 0)

# Configurações do jogo
INITIAL_OBSTACLES = 6
INITIAL_HEALTH = 3

# Massas dos objetos
MASS_ITEM = 1
MASS_OBSTACLE = 3
MASS_POWERUP = 2

SIZE_POWERUPS = 40
TIME_TO_START = 3
POWERUP_DURATION = 15
MAX_POWERUPS_PER_LEVEL = 3
PLAYER_BASE_SPEED = 7
PLAYER_SPEED_INCREMENT = 0.5
PLAYER_RADIUS = 25
POINTS_FOR_CORRECT_ANSWER = 3

# Arquivos
extra_life_sound_path = "sounds/extra_life.wav"
health_collect_sound_path = "sounds/extra_life2.wav"
obstacle_destroyed_sound_path = "sounds/obstacle_destroyed.wav"
score_file = "data/high_scores.txt"
question_file = "data/questions.xlsx"
acertou_sound_path = "sounds/acertou.wav"
errou_sound_path = "sounds/faustao_errou.wav"
obstacle_collision_sound_path = "sounds/damage.wav"
item_collect_sound_path = "sounds/collect.wav"
game_over_sound_path = "sounds/game_over.wav"
congratulations_sound_file = "sounds/zerou.wav"
level_up_sound_path = "sounds/level_up.wav"
congratulations_image_file = "images/img_zerou.png"
help_file = "data/help.txt"

# Intervalo de tempo para decremento do score
score_decrement_interval = 20

# Inicializações
high_scores = []
questions = []
answered_questions = set()
#player_velocity = pygame.math.Vector2(0, 0)
active_powerups = []

addition_obstacles_for_wrong_answer = 3
# Contadores e tempos
GAME_START_TIME = 0
INITIAL_LAST_ITEM_COLLECT_TIME = 0
INITIAL_SCORE = 10
INITIAL_START_TIME = 0
INITIAL_LAST_ITEM_COLLECT_TIME = 0
INITIAL_CORRECT_ANSWERS_STREAK = 0
INITIAL_COLLISION_COUNT = 0
INITIAL_CORRECT_ANSWERS = 0
INITIAL_LEVEL = 1
