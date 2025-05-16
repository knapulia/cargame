# car_config.py

selected_car_color_path = "assets/car_red.PNG"  # за замовчуванням

def set_car_color_path(path):
    global selected_car_color_path
    selected_car_color_path = path

def get_car_color_path():
    return selected_car_color_path
