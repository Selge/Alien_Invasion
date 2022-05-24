import pygame


class Ship:
    """Класс управления главным героем (кораблём)"""
    def __init__(self, ai_game):
        # Инициализируем корабль и задаём его стартовую позицию:
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Загружаем изображение корабля и оформляем его в прямоугольник:
        self.image = pygame.image.load('images/ship_blue.bmp')  # Достаём нужную картинку
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана:
        self.rect.midbottom = self.screen_rect.midbottom
        # Сохранение координаты центра корабля
        self.x = float(self.rect.x)
        # Флаг движения вправо
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляем позицию с учётом флага"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # На основании self.x обновляем rect, который отвечает за позицию корабля:
        self.rect.x = self.x

    def blitme(self):
        """Выводим на экран корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)
