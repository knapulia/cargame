import pygame


WIDTH, HEIGHT = 768, 768


BLACK_BLUE = (7, 91, 89)
DARK_BLUE = (13, 150, 147)


class Button:
    def __init__(
            self, x, y, normal_image, pressed_image, text, font,
            size=(150, 50), action=None
    ):
        self.normal_image = pygame.image.load(normal_image)
        self.pressed_image = pygame.image.load(pressed_image)
        self.normal_image = pygame.transform.scale(self.normal_image, size)
        self.pressed_image = pygame.transform.scale(self.pressed_image, size)
        self.size = size
        self.x = x
        self.y = y
        self.image = self.normal_image
        self.rect = self.normal_image.get_rect(
            center=(WIDTH // 2 + self.x, self.y)
        )
        self.text = text
        self.font = font
        self.text_color_normal = DARK_BLUE
        self.text_color_pressed = BLACK_BLUE
        self.text_color = self.text_color_normal
        self.action = action
        self.pressed = False

    def update_position(self, new_width, new_height):
        self.rect.center = (new_width // 2 + self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN
                and self.rect.collidepoint(event.pos)):
            self.image = self.pressed_image
            self.text_color = self.text_color_pressed
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and self.pressed:
            self.image = self.normal_image
            self.text_color = self.text_color_normal
            self.pressed = False
            if self.action:
                self.action()
