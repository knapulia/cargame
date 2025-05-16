import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from utils import load_image, load_font
from button import Button

class Menu:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption("Car Game Menu")

        self.bg_original = load_image("menu_background.PNG")

        self.font = load_font(32)
        self.title_font = load_font(64)
        self.title_text = "Menu"

        self.buttons = [
            Button(0, 0, "Easy", self.font, width=200, height=70),
            Button(0, 0, "Middle", self.font, width=200, height=70),
            Button(0, 0, "Hard", self.font, width=200, height=70),
            Button(0, 0, "Setting", self.font, width=200, height=70),
            Button(0, 0, "Exit", self.font, width=200, height=70)
        ]

        self.cloud_image = load_image("cloud.png")
        self.clouds = []
        self.cloud_spawn_timer = 0

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                for button in self.buttons:
                    button.handle_event(event)

            width, height = self.screen.get_size()
            bg_scaled = pygame.transform.scale(self.bg_original, (width, height))
            self.screen.blit(bg_scaled, (0, 0))

            # ➕ Створення хмар з рандомними розмірами та позицією
            self.cloud_spawn_timer += 0.5
            if self.cloud_spawn_timer >= 240:  # частота появи
                self.cloud_spawn_timer = 0
                cloud_y = random.randint(20, height // 3)  # випадкова висота
                scale = random.uniform(0.5, 1.2)           # випадковий масштаб
                scaled_cloud = pygame.transform.scale(
                    self.cloud_image,
                    (int(self.cloud_image.get_width() * scale),
                     int(self.cloud_image.get_height() * scale))
                )
                self.clouds.append({"x": -100, "y": cloud_y, "img": scaled_cloud})

            # ➕ Малювання і рух хмар
            for cloud in self.clouds:
                cloud["x"] += 1
                self.screen.blit(cloud["img"], (cloud["x"], cloud["y"]))

            self.clouds = [c for c in self.clouds if c["x"] < width + 200]

            # Назва гри
            title_surface = self.title_font.render(self.title_text, True, (225, 225, 255))
            title_rect = title_surface.get_rect(center=(width // 2, height // 10))
            self.screen.blit(title_surface, title_rect)

            # Центрування кнопок
            center_x = width // 2
            start_y = height // 4
            gap = 80

            for i, button in enumerate(self.buttons):
                button.update_position(center_x, start_y + i * gap)
                button.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
