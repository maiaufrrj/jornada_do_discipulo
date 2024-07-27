# audio.py
import pygame

def load_sound(sound_path):
    try:
        return pygame.mixer.Sound(sound_path)
    except pygame.error as e:
        print(f"Warning: Could not load sound: {sound_path}. {e}")
        return None
