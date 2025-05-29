import pygame
from cargame.obstacle import EnemyCar


def test_enemycar_creation(monkeypatch):
    pygame.init()
    monkeypatch.setattr("pygame.image.load", lambda path: pygame.Surface((50, 50)))
    car = EnemyCar("dummy.png", speed=5)
    assert isinstance(car.rect.centerx, int)
    assert car.rect.bottom == 0

def test_enemycar_update_removal(monkeypatch):
    pygame.init()
    monkeypatch.setattr("pygame.image.load", lambda path: pygame.Surface((50, 50)))
    car = EnemyCar("dummy.png", speed=1000)
    screen = pygame.display.set_mode((768, 768))

    car.update()
    assert car.alive() is False or car.rect.top > 768
