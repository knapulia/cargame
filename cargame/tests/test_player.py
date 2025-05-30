import pygame
from cargame.player import Player


def test_player_init(monkeypatch):
    pygame.init()
    monkeypatch.setattr("pygame.image.load",
                        lambda path: pygame.Surface((50, 50)))
    player = Player("dummy.png")
    assert player.current_lane_index == 1
    assert player.rect.bottom <= 768


def test_player_movement(monkeypatch):
    pygame.init()
    monkeypatch.setattr("pygame.image.load",
                        lambda path: pygame.Surface((50, 50)))
    player = Player("dummy.png")

    initial_lane = player.current_lane_index
    player.move_left()
    assert (player.current_lane_index
            == max(0, initial_lane - 1))

    player.move_right()
    assert (player.current_lane_index
            == min(2, player.current_lane_index))
