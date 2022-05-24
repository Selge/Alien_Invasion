import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс, представляющий одного пришельца"""
    def __init__(self, ai_game):
        """Создаёт пришельца и задаёт его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        # Загружаем изображение пришельца и назначаем ему атрибут rect
        self.image = pygame.image.load('images/alien_green_blue.bmp')
        self.rect = self.image.get_rect()
        # Загрузка прищельцев начинается с левого верхнего угла экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Сохраняем точную (без точек) горизонтальную позицию пришельца
        self.x = float(self.rect.x)
