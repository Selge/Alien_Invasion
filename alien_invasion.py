import sys
from time import sleep

import pygame
import pygame_menu
import pygame.font
from pygame import transform
from pygame.sprite import Group
from pygame.sprite import Sprite


class Settings:
    def __init__(self):
        # screen
        self.screen_width = 1000
        self.screen_height = 600
        self._color = (28, 28, 28)
        self.bg = Background('images/nightsky_background.jpg', [0, 0])
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
        # other
        self.speedup_scale = 1.5
        self.score_scale = 1.5
        self.fleet_drop_speed = 4
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 5.0
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


class Background(pygame.sprite.Sprite):
    def __init__(self, image, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Sounds:
    pygame.mixer.init()
    bullet_sound = pygame.mixer.Sound('sounds/bullet.wav')
    rocket_sound = pygame.mixer.Sound('sounds/rocket.wav')
    alien_sound = pygame.mixer.Sound('sounds/explosion.wav')
    ship_collides_sound = pygame.mixer.Sound('sounds/explosion.wav')
    soundtrack_sound = pygame.mixer.Sound('sounds/through space.ogg')


class GameStats:
    def __init__(self, ufo_game):
        self.settings = ufo_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.rockets_left = self.settings.rocket_limit
        self.score = 0
        self.level = 1


class Menu:
    pygame.init()
    surface = pygame.display.set_mode((1000, 800))

    def set_ship_color(self):
        pass

    def set_difficulty(self):
        pass

    def start_the_game(self):
        pass


class Scoreboard:
    def __init__(self, ufo_game):
        self.ufo_game = ufo_game
        self.screen = ufo_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ufo_game.settings
        self.stats = ufo_game.stats
        self.text_color = (255, 250, 250)
        self.font = pygame.font.SysFont('SH Pinscher', 20)
        self.prep_score()
        self.prep_level()
        self.prep_ships()
        self.prep_rockets()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings._color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings._color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = ScoreShip(self.ufo_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_rockets(self):
        self.rockets = Group()
        for rocket_number in range(self.stats.rockets_left):
            rocket = ScoreRocket(self.ufo_game)
            rocket.rect.x = 200 + rocket_number * rocket.rect.width
            rocket.rect.y = 10
            self.rockets.add(rocket)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        self.rockets.draw(self.screen)


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("U.F.O. 77")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Start")
        self.pause_button = Button(self, "Pause")

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_rockets()
                self._update_aliens()
            self._update_screen()

    def start_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.aliens.empty()
        self.bullets.empty()
        self.rockets.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)
        Sounds.soundtrack_sound.play()

    def paused(self):
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        pause = False
                    elif event.key == pygame.K_q:
                        sys.exit()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_rockets()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_r:
            self._fire_rocket()
        elif event.key == pygame.K_o:
            self.start_game()
        elif event.key == pygame.K_p:
            self.paused()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            Sounds.bullet_sound.play()

    def _fire_rocket(self):
        if len(self.rockets) < self.settings.rocket_limit:
            new_rocket = Rocket(self)
            self.rockets.add(new_rocket)
            self.settings.rocket_limit -= 1
            self._rocket_hit()
            Sounds.rocket_sound.play()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _update_rockets(self):
        self.rockets.update()
        for rocket in self.rockets.copy():
            if rocket.rect.bottom <= 0:
                self.rockets.remove(rocket)
        self._check_rocket_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            Sounds.alien_sound.play()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _check_rocket_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.rockets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            Sounds.alien_sound.play()
        if not self.aliens:
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        Sounds.ship_collides_sound.play()
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.rockets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _rocket_hit(self):
        if self.stats.rockets_left > 0:
            self.stats.rockets_left -= 1
            self.sb.prep_rockets()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (3 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        self.screen.fill(self.settings._color)
        self.screen.blit(self.settings.bg.image, self.settings.bg.rect)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for rocket in self.rockets.sprites():
            rocket.draw_rocket()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


class Ship(Sprite):
    def __init__(self, ufo_game):
        super().__init__()
        self.screen = ufo_game.screen
        self.settings = ufo_game.settings
        self.screen_rect = ufo_game.screen.get_rect()
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
    def __init__(self, ufo_game):
        super().__init__(ufo_game)
        self.image = pygame.image.load('images/ship_new.png')
        self.image = transform.scale(self.image, (25, 20))
        self.rect = self.image.get_rect()


class ScoreRocket(Ship):
    def __init__(self, ufo_game):
        super().__init__(ufo_game)
        self.image = pygame.image.load('images/bomb.png')
        self.image = transform.scale(self.image, (25, 20))
        self.rect = self.image.get_rect()


class Alien(Sprite):
    def __init__(self, ufo_game):
        super().__init__()
        self.screen = ufo_game.screen
        self.settings = ufo_game.settings
        self.image = pygame.image.load('images/alien_white_28.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x


class Bullet(Sprite):
    def __init__(self, ufo_game):
        super().__init__()
        self.screen = ufo_game.screen
        self.settings = ufo_game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ufo_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Rocket(Sprite):
    def __init__(self, ufo_game):
        super().__init__()
        self.screen = ufo_game.screen
        self.settings = ufo_game.settings
        self.color = self.settings.rocket_color
        self.rect = pygame.Rect(0, 0, self.settings.rocket_width, self.settings.rocket_height)
        self.rect.midtop = ufo_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.rocket_speed
        self.rect.y = self.y

    def draw_rocket(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Button:
    def __init__(self, ufo_game, msg):
        self.screen = ufo_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (128, 128, 128)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('SH Pinscher', 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


if __name__ == '__main__':
    AlienInvasion().run_game()
