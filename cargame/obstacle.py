# cargame/obstacle.py
import pygame
import random
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, LANES_X


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, image_path, speed):
        super().__init__()
        try:
            # Завантажуємо зображення і одразу повертаємо його на 180 градусів
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.rotate(original_image, 180)
            self.image = pygame.transform.scale(self.image,
                                                (PLAYER_WIDTH, PLAYER_HEIGHT))
        except pygame.error as e:
            print(f"Помилка завантаження зображення ворога: "
                  f"{image_path} - {e}")
            self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
            self.image.fill((255, 0, 0))
            # Червоний прямокутник як запасний варіант

        self.rect = self.image.get_rect()

        self.lanes = LANES_X
        # Випадково обираємо смугу для появи ворога
        self.rect.centerx = random.choice(self.lanes)
        self.rect.bottom = 0  # Починає зверху, за межами екрану

        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        # Видаляємо ворога, якщо він вийшов за межі екрану знизу
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()  # Видалення спрайту з усіх груп

    def draw(self, screen):
        screen.blit(self.image, self.rect)
