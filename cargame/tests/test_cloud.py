import pygame
from cargame.cloud import Cloud


def test_cloud_reset_and_update(monkeypatch):
    pygame.init()
    monkeypatch.setattr("pygame.image.load",
                        lambda path: pygame.Surface((150, 50)))
    cloud = Cloud(800, 600, "dummy.png")

    initial_x = cloud.x
    cloud.update(800)
    assert cloud.x > initial_x

    cloud.x = 801
    cloud.update(800)
    assert cloud.x <= 0  # після reset()
