import pygame
import pytest
from cargame.button import Button


@pytest.fixture
def button(monkeypatch):
    pygame.init()
    surface = pygame.Surface((200, 70))
    monkeypatch.setattr(pygame.image, "load", lambda path: surface)

    font = pygame.font.Font(None, 36)
    return Button(
        0, 0,
        "dummy.png", "dummy.png",
        "TEST", font,
        size=(200, 70),
        action=lambda: print("clicked")
    )

def test_button_event_press_release(button):
    down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=button.rect.center)
    up = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=button.rect.center)

    button.handle_event(down)
    assert button.pressed is True

    button.handle_event(up)
    assert button.pressed is False
