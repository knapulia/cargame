# cargame/player.py
import pygame
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, LANES_X, HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Помилка завантаження зображення гравця: {image_path} - {e}")
            # Запасний варіант, якщо зображення не знайдено
            self.original_image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
            self.original_image.fill((0, 255, 0)) # Зелений прямокутник

        self.image = pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()

        self.lanes = LANES_X
        self.current_lane_index = 1  # Починаємо на середній смузі
        self.rect.centerx = self.lanes[self.current_lane_index]
        self.rect.bottom = HEIGHT - 30  # Позиція внизу екрану

        self.speed = 5 # Швидкість зміни смуги (можна налаштувати)

    def move_left(self):
        if self.current_lane_index > 0:
            self.current_lane_index -= 1
            # Плавний рух можна реалізувати тут, або миттєвий:
            self.rect.centerx = self.lanes[self.current_lane_index]

    def move_right(self):
        if self.current_lane_index < len(self.lanes) - 1:
            self.current_lane_index += 1
            self.rect.centerx = self.lanes[self.current_lane_index]

    def handle_input(self, keys):
        # Обробка натискання клавіш буде в ігровому циклі,
        # оскільки нам потрібне одноразове реагування на натискання, а не утримання
        pass

    def update(self):
        # Тут можна додати анімацію або іншу логіку оновлення, якщо потрібно
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset(self):
        self.current_lane_index = 1
        self.rect.centerx = self.lanes[self.current_lane_index]
        self.rect.bottom = HEIGHT - 30