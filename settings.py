class Settings:
    """We store all the settings here"""
    def __init__(self):
        # Screen settings
        # Screen size variables:
        self.screen_width = 1200
        self.screen_height = 800
        # Variable that sets up the background color:
        self.bg_color = (204, 255, 255)  # RGB colors.
        self.ship_speed = 2
        # Параметры выстрела:
        self.bullet_speed = 4  # скорость полёта снаряда
        self.bullet_width = 3  # ширина снаряда 3 пикселя
        self.bullet_height = 15  # высота снаряда 15 пикселей
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3  # ограничиваем количество снарядов на экране одномоментно
