from cargame.car_config import set_car_color_path, get_car_color_path


def test_set_and_get_car_color_path():
    path = "assets/car_green.PNG"
    set_car_color_path(path)
    assert get_car_color_path() == path
