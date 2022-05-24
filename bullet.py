import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Управляем выстреливаемыми снарядами"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        # Создадим снаряд в позиции (0, 0) и назначим ему правильную позицию:
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop  # снаряд стартует из самой верхней и центральной точки корабля
        # Позиция снаряда определяется как число без точки:
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        # Обновляем позиции снаряда по оси y:
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Выводим снаряд на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
