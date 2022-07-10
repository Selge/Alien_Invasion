class Settings:
    def __init__(self):
        # screen
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (28, 28, 28)
        # ship
        self.ship_limit = 5
        # bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 250, 250)
        self.bullets_allowed = 50
        # rocket
        self.rocket_width = 500
        self.rocket_height = 10
        self.rocket_color = (255, 250, 250)
        self.rocket_limit = 12

        self.speedup_scale = 1.5
        self.score_scale = 1.5
        self.fleet_drop_speed = 4
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 3.0
        self.bullet_speed = 10.0
        self.rocket_speed = 15.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.rocket_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
