# cargame/game.py
import pygame
import sys
import random
from car_config import get_car_color_path
from player import Player
from obstacle import EnemyCar
from scenery import Bush
from settings import WIDTH, HEIGHT, FPS, LANES_X, PLAYER_HEIGHT

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)


def run_easy_level():  # Назва функції змінена для ясності
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # НЕ RESIZABLE для гри
    pygame.display.set_caption("Easy Level")
    clock = pygame.time.Clock()

    # Швидкість гри для легкого рівня
    game_speed = 5  # Пікселів за кадр для ворогів та фону

    # --- Ресурси ---
    try:
        # Фон дороги
        road_bg_original = pygame.image.load("assets/level_background.PNG").convert()
        road_bg = pygame.transform.scale(road_bg_original, (WIDTH, HEIGHT))

        bush_image_path = "assets/bushes.PNG"
    except pygame.error as e:
        print(f"Помилка завантаження ресурсів рівня: {e}")
        pygame.quit()
        sys.exit()

    # Прокручування фону дороги
    bg_y1 = 0
    bg_y2 = -HEIGHT

    # Гравець
    player_car_path = get_car_color_path()
    player = Player(player_car_path)
    player_group = pygame.sprite.GroupSingle(player)  # Група для одного гравця

    # Вороги
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0
    ENEMY_SPAWN_DELAY_EASY = 2000  # мс (2 секунди) - вороги з'являються не часто

    # Кущі
    bushes = pygame.sprite.Group()
    BUSH_COUNT = 1  # Кількість кущів одночасно на екрані
    for _ in range(BUSH_COUNT):
        bush = Bush(bush_image_path, game_speed)
        bush.rect.y = random.randint(-HEIGHT, HEIGHT)
        bushes.add(bush)

    # Стан гри
    game_active = False  # Чи почався рух (після натискання Пробілу)
    game_over = False

    # Шрифт для повідомлень
    try:
        font_path = "assets/pixel_font.ttf"
        game_font_large = pygame.font.Font(font_path, 72)
        game_font_small = pygame.font.Font(font_path, 36)
    except FileNotFoundError:
        print(f"Помилка: файл шрифту '{font_path}' не знайдено. Використовується стандартний шрифт.")
        game_font_large = pygame.font.SysFont(None, 72)
        game_font_small = pygame.font.SysFont(None, 36)

    # --- Головний цикл гри ---
    running = True
    while running:
        dt = clock.tick(FPS)  # Дельта часу, не використовується активно тут, але добре мати

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                if not game_active:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_active = True
                else:  # game_active is True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            player.move_left()
                        if event.key == pygame.K_RIGHT:
                            player.move_right()
            else:  # game_over is True
                if event.type == pygame.KEYDOWN:  # Будь-яка клавіша для повернення в меню
                    # Тут можна додати повернення в головне меню
                    # Наприклад, викликати main_menu() з menu.py
                    # Для цього game.py має знати про main_menu або повернути сигнал
                    from menu import main_menu  # Імпортуємо тут, щоб уникнути циклічних залежностей
                    main_menu()
                    return  # Вихід з run_easy_level

        if not game_over:
            if game_active:
                # --- Оновлення об'єктів ---
                player.update()  # Наразі не робить багато, але може знадобитися

                # Генерація ворогів
                enemy_spawn_timer += dt
                if enemy_spawn_timer >= ENEMY_SPAWN_DELAY_EASY:
                    enemy_spawn_timer = 0
                    # Гарантуємо, що не спавнимо на всіх смугах одночасно
                    # Для легкого рівня просто спавнимо одного ворога на випадковій смузі
                    if len(enemies) < 3:  # Обмеження на кількість ворогів одночасно
                        new_enemy = EnemyCar(player_car_path, game_speed)  # Вороги використовують той самий скін

                        # Перевірка, щоб не спавнити ворога прямо на гравця або дуже близько
                        can_spawn = True
                        # Проста перевірка, щоб не було миттєвого зіткнення при спавні
                        # (можна покращити, перевіряючи смугу гравця)
                        temp_rect = new_enemy.rect.copy()
                        temp_rect.y += PLAYER_HEIGHT  # Перевірка трохи попереду
                        if temp_rect.colliderect(player.rect) and new_enemy.rect.centerx == player.rect.centerx:
                            can_spawn = False

                        if can_spawn:
                            # Перевірка, чи ця смуга вже не зайнята нещодавно створеним ворогом
                            lane_occupied = False
                            for enemy in enemies:
                                if enemy.rect.centerx == new_enemy.rect.centerx and enemy.rect.bottom < PLAYER_HEIGHT * 2:
                                    lane_occupied = True
                                    break
                            if not lane_occupied:
                                enemies.add(new_enemy)

                enemies.update()  # Рух ворогів
                bushes.update()  # Рух кущів

                # Прокручування фону дороги
                bg_y1 += game_speed
                bg_y2 += game_speed
                if bg_y1 >= HEIGHT:
                    bg_y1 = -HEIGHT
                if bg_y2 >= HEIGHT:
                    bg_y2 = -HEIGHT

                # Перевірка зіткнень
                if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
                    # pygame.sprite.collide_mask для більш точного зіткнення по пікселях
                    print("Зіткнення! Гру закінчено!")
                    game_over = True
                    game_active = False  # Зупиняємо рух

            # --- Малювання ---
            screen.fill(BLACK)  # Чорний фон на випадок, якщо дорога не покриває все

            # Малюємо дорогу
            screen.blit(road_bg, (0, bg_y1))
            screen.blit(road_bg, (0, bg_y2))

            bushes.draw(screen)  # Малюємо кущі
            player_group.draw(screen)  # Малюємо гравця
            enemies.draw(screen)  # Малюємо ворогів

            if not game_active and not game_over:
                # Повідомлення "Press SPACE to Start"
                start_text = game_font_small.render("PRESS SPACE TO START", True, WHITE)
                start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                pygame.draw.rect(screen, BLACK, start_rect.inflate(20, 10))  # Фон для тексту
                screen.blit(start_text, start_rect)

        else:  # game_over is True
            screen.fill(BLACK)  # Можна додати фон для "GAME OVER"
            game_over_text = game_font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(game_over_text, game_over_rect)

            prompt_text = game_font_small.render("Press any key to return to menu", True, WHITE)
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(prompt_text, prompt_rect)

        pygame.display.flip()

    # pygame.quit() # Не викликаємо тут, якщо повертаємось в меню
    # sys.exit()