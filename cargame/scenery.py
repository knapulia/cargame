# cargame/scenery.py
import pygame
import random
from settings import WIDTH, HEIGHT


class Bush(pygame.sprite.Sprite):
    def __init__(self, image_path, speed):
        super().__init__()
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            # Масштабування кущів (можна налаштувати)
            self.image = pygame.transform.scale(self.original_image, (80, 80))
        except pygame.error as e:
            print(f"Помилка завантаження зображення куща: {image_path} - {e}")
            self.image = pygame.Surface([50, 50])
            self.image.fill((34, 139, 34))  # Темно-зелений

        self.rect = self.image.get_rect()

        # Кущі з'являються або зліва, або справа
        if random.choice([True, False]):
            # Ліва сторона, трохи за межами основної дороги (припустимо ширина дороги ~WIDTH/2)
            self.rect.centerx = random.randint(20, WIDTH // 4 - 50)
        else:
            # Права сторона
            self.rect.centerx = random.randint(3 * WIDTH // 4 + 50, WIDTH - 20)

        self.rect.bottom = random.randint(-HEIGHT, 0)  # Починають зверху, за межами екрану
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            # Переміщуємо кущ нагору для повторного використання
            self.rect.bottom = 0
            if random.choice([True, False]):
                self.rect.centerx = random.randint(20, WIDTH // 4 - 50)
            else:
                self.rect.centerx = random.randint(3 * WIDTH // 4 + 50, WIDTH - 20)
            self.rect.y = random.randint(-200, -50)  # Знову за межами екрану зверху

    def draw(self, screen):
        screen.blit(self.image, self.rect)