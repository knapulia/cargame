# cargame/game.py
import pygame
import sys
import random
from car_config import get_car_color_path
from player import Player
from obstacle import EnemyCar
from settings import WIDTH, HEIGHT, FPS, LANES_X, PLAYER_HEIGHT
from score import ScoreManager

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)


def run_easy_level():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Easy Level")
    clock = pygame.time.Clock()

    game_speed = 5

    try:
        road_bg_original = pygame.image.load("assets/level_background.PNG").convert()
        road_bg = pygame.transform.scale(road_bg_original, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Помилка завантаження ресурсів рівня: {e}")
        pygame.quit()
        sys.exit()

    bg_y = 0  # координата фону

    player_car_path = get_car_color_path()
    player = Player(player_car_path)
    player_group = pygame.sprite.GroupSingle(player)

    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0
    ENEMY_SPAWN_DELAY_EASY = 2000

    game_active = False
    game_over = False
    score = ScoreManager("easy")  # створюємо об'єкт для підрахунку часу

    try:
        font_path = "assets/pixel_font.ttf"
        game_font_large = pygame.font.Font(font_path, 72)
        game_font_small = pygame.font.Font(font_path, 36)
    except FileNotFoundError:
        print(f"Файл шрифту '{font_path}' не знайдено. Використовується стандартний шрифт.")
        game_font_large = pygame.font.SysFont(None, 72)
        game_font_small = pygame.font.SysFont(None, 36)

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                if not game_active:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_active = True
                        score.start()
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            player.move_left()
                        if event.key == pygame.K_RIGHT:
                            player.move_right()
            else:
                if event.type == pygame.KEYDOWN:
                    from menu import easy_menu
                    easy_menu()
                    return

        if not game_over:
            if game_active:
                player.update()
                score.update()

                enemy_spawn_timer += dt
                if enemy_spawn_timer >= ENEMY_SPAWN_DELAY_EASY:
                    enemy_spawn_timer = 0
                    if len(enemies) < 3:
                        new_enemy = EnemyCar(player_car_path, game_speed)

                        can_spawn = True
                        temp_rect = new_enemy.rect.copy()
                        temp_rect.y += PLAYER_HEIGHT
                        if temp_rect.colliderect(player.rect) and new_enemy.rect.centerx == player.rect.centerx:
                            can_spawn = False

                        if can_spawn:
                            lane_occupied = False
                            for enemy in enemies:
                                if enemy.rect.centerx == new_enemy.rect.centerx and enemy.rect.bottom < PLAYER_HEIGHT * 2:
                                    lane_occupied = True
                                    break
                            if not lane_occupied:
                                enemies.add(new_enemy)

                enemies.update()

                # Перевірка зіткнень
                if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
                    # pygame.sprite.collide_mask для більш точного зіткнення по пікселях
                    print("Зіткнення! Гру закінчено!")
                    game_over = True
                    game_active = False  # Зупиняємо рух
                    score.save_best_score()

                bg_y += game_speed  # Прокручуємо фон тільки під час активної гри

            scroll = bg_y % HEIGHT  # Завжди обчислюємо scroll

            # Малювання
            screen.blit(road_bg, (0, scroll - HEIGHT))
            screen.blit(road_bg, (0, scroll))

            player_group.draw(screen)
            enemies.draw(screen)

            if not game_active and not game_over:
                start_text = game_font_small.render("PRESS SPACE TO START", True, WHITE)
                start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                pygame.draw.rect(screen, BLACK, start_rect.inflate(20, 10))
                screen.blit(start_text, start_rect)



        else:  # game_over is True
            screen.fill(BLACK)  # Можна додати фон для "GAME OVER"
            game_over_text = game_font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(game_over_text, game_over_rect)

            prompt_text = game_font_small.render("Press any key to return to menu", True, WHITE)
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(prompt_text, prompt_rect)

        score.draw_score(screen)
        pygame.display.flip()



    # pygame.quit() # Не викликаємо тут, якщо повертаємось в меню
    # sys.exit()