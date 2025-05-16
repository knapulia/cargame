import pygame
import random

WIDTH, HEIGHT = 768, 768

class Cloud:
    def __init__(self, screen_width, screen_height, image_path):
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)

        size_factor = random.uniform(0.8, 1.5)
        self.width = int(150 * size_factor)
        self.height = int(60 * size_factor)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.x = -self.width
        self.y = random.randint(10, 250)
        self.speed = random.uniform(2, 4)

    def update(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.reset()

    def reset(self):
        self.x = -self.width
        self.y = random.randint(50, 250)
        size_factor = random.uniform(0.8, 1.5)
        self.width = int(100 * size_factor)
        self.height = int(60 * size_factor)
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (self.width, self.height))
        self.speed = random.uniform(2, 4)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
