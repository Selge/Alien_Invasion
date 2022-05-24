import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Главный класс для управления ресурсами и поведением приложения"""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        # Импортируем настройки экрана
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Создаём кораблик и загружаем боекомплект:
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # Нужна группа, чтобы стрелять очередями
        self.aliens = pygame.sprite.Group()  # Чужие тоже воюют толпой

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            # Вспомогательные модули: во время работы игры отслеживаются команды и меняется экран
            self._check_events()
            self.ship.update()  # Обновляем положение корабля
            self._update_bullets()
            self._create_fleet()
            self._update_screen()

    def _check_events(self):
        """Обрабатываем команды с клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Нажимаем клавиши"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_w:
            self.screen = pygame.display.set_mode((900, 600))
            self.ship = Ship(self)
        elif event.key == pygame.K_SPACE:
            self._fire_bullet( )
        elif event.key == pygame.K_RSHIFT or pygame.K_LSHIFT:
            self._fire_bullet = True
        elif event.key == pygame.K_f:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.ship = Ship(self)

    def _check_keyup_events(self, event):
        """Отпускаем клавиши"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RSHIFT or pygame.K_LSHIFT:
            self._fire_bullet = False

    def _update_bullets(self):
        """Обновляем позиции снарядов и удаляем улетевшие"""
        # Обновление позиций снарядов:
        self.bullets.update()
        # Удаляем вылетевшие с поля снаряды
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:  # Достигаем верхней точки экрана
                self.bullets.remove(bullet)
            #  print(len(self.bullets))  # Видим количество летящих снарядов в консоли, очень интересно!

    def _create_fleet(self):
        """Creating an aline fleet"""
        # Creating an alien ship
        alien = Alien(self)
        self.aliens.add(alien)

    def _update_screen(self):
        """Управляем экраном"""
        # При каждом проходе цикла перерисовывается экран:
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # Чтобы нарисовать все выпущенные снаряды, перебираем спрайты и вызываем для каждого
        self.aliens.draw(self.screen)
        # Отображаем последний прорисованный экран
        pygame.display.flip()

    def _fire_bullet(self):
        """Создаём новый снаряд и включаем его в группу"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        self._fire_bullet = False


if __name__ == '__main__':
    # Создаём экземпляр и запускаем игру
    ai = AlienInvasion()
    ai.run_game()
