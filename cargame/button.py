from utils import load_image
import pygame

class Button:
    def __init__(self, x, y, text, font, width=None, height=None):
        original_normal = load_image("normal_button.PNG")
        original_pressed = load_image("pressed_button.PNG")

        # Якщо задано розміри — масштабуємо зображення
        if width and height:
            self.image_normal = pygame.transform.scale(original_normal, (width, height))
            self.image_pressed = pygame.transform.scale(original_pressed, (width, height))
        else:
            self.image_normal = original_normal
            self.image_pressed = original_pressed

        self.font = font
        self.text = text
        self.rect = self.image_normal.get_rect(topleft=(x, y))
        self.pressed = False

    def update_position(self, center_x, y):
        self.rect = self.image_normal.get_rect(center=(center_x, y))

    def draw(self, surface):
        image = self.image_pressed if self.pressed else self.image_normal
        surface.blit(image, self.rect)

        # Колір тексту: білий при натисканні, чорний — стандартно
        if self.pressed:
            text_color = (7, 91, 89)
        else:
            text_color = (13, 150, 147)

        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.pressed = True
            print(f"{self.text} clicked!")
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False



    def update_position(self, center_x, y):
        self.rect = self.image_normal.get_rect(center=(center_x, y))

