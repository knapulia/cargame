import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, LANES
from utils import load_image, load_font, draw_text
from player import PlayerCar
from obstacle import ObstacleCar

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Car Racing Game")

        self.bg = load_image("menu_background.PNG")
        self.player_image = load_image("menu_background.PNG")  # заміни на окремий файл авто
        self.obstacle_image = load_image("menu_background.PNG")  # заміни на авто-противника

        self.player = PlayerCar(self.player_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.obstacles = []

        self.score = 0
        self.font = load_font(24)

    def spawn_obstacle(self):
        x = random.choice(LANES)
        self.obstacles.append(ObstacleCar(self.obstacle_image, x, -100))

    def check_collision(self):
        for obs in self.obstacles:
            if self.player.rect.colliderect(obs.rect):
                return True
        return False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        for obs in self.obstacles:
            obs.move()
        self.obstacles = [obs for obs in self.obstacles if not obs.off_screen()]

        if random.randint(1, 30) == 1:
            self.spawn_obstacle()

        self.score += 1

    def draw(self, surface):
        image = self.image_pressed if self.pressed else self.image_normal
        surface.blit(image, self.rect)

        # Колір тексту залежить від стану кнопки
        text_color = (255, 255, 255) if self.pressed else (0, 0, 0)

        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()
            pygame.display.flip()

            if self.check_collision():
                print("Game Over")
                running = False

        pygame.quit()
