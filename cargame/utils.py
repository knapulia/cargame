import pygame
import os
from settings import ASSETS_PATH

def load_image(filename):
    return pygame.image.load(os.path.join(ASSETS_PATH, filename)).convert_alpha()

def load_font(size):
    return pygame.font.Font(os.path.join(ASSETS_PATH, "pixel_font.ttf"), size)
