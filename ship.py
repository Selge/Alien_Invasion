import pygame
from pygame import transform

from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('images/ship_new.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


class ScoreShip(Ship):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.image = pygame.image.load('images/ship_new.png')
        self.image = transform.scale(self.image, (25, 20))
        self.rect = self.image.get_rect()


class ScoreRocket(Ship):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.image = pygame.image.load('images/bomb.png')
        self.image = transform.scale(self.image, (25, 20))
        self.rect = self.image.get_rect()
