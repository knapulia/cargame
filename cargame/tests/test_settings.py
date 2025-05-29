from cargame import settings

def test_settings_values():
    assert settings.WIDTH > 0
    assert settings.HEIGHT > 0
    assert settings.FPS > 0
    assert len(settings.LANES_X) == 3