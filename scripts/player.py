import pygame
from scripts.config import *
from scripts.utils import load_ship_image
from scripts.projectiles import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, ship_type='level1'):
        super().__init__()

        # Load ship stats
        self.stats = SHIP_STATS.get(ship_type, SHIP_STATS['level1'])

        # Load ship image
        self.image = load_ship_image(ship_type)
        self.rect = self.image.get_rect()

        # Position the player
        self.rect.centerx = 100
        self.rect.centery = SCREEN_HEIGHT // 2

        # Movement attributes
        self.speedx = 0
        self.speedy = 0
        self.speed = self.stats['speed']

        # Combat attributes
        self.shield = self.stats['health']
        self.max_shield = self.stats['health']
        self.power_level = self.stats['power']
        self.shoot_delay = self.stats['fire_rate']
        self.last_shot = pygame.time.get_ticks()

        # Player stats
        self.lives = PLAYER_LIVES
        self.score = 0
        self.ship_type = ship_type

        # Load a smaller version of the ship image for the lives display
        self.mini_ship = pygame.transform.scale(self.image, (30, 20))

    def update(self):
        # Reset speed
        self.speedx = 0
        self.speedy = 0

        # Get keyboard input
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -self.speed
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = self.speed
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy = -self.speed
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy = self.speed

        # Auto-shooting feature (can be toggled)
        if keystate[pygame.K_SPACE]:
            self.shoot()

        # Update position
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullets = []

            # Different shooting patterns based on power level
            if self.power_level == 1:
                # Single bullet
                bullet = Bullet(self.rect.right, self.rect.centery, 'blue')
                bullets.append(bullet)

            elif self.power_level == 2:
                # Double bullets
                bullet1 = Bullet(self.rect.right, self.rect.centery - 10, 'blue')
                bullet2 = Bullet(self.rect.right, self.rect.centery + 10, 'blue')
                bullets.extend([bullet1, bullet2])

            elif self.power_level >= 3:
                # Triple bullets with spread
                bullet1 = Bullet(self.rect.right, self.rect.centery, 'blue', 10, 0)
                bullet2 = Bullet(self.rect.right, self.rect.centery - 15, 'blue', 10, -1)
                bullet3 = Bullet(self.rect.right, self.rect.centery + 15, 'blue', 10, 1)
                bullets.extend([bullet1, bullet2, bullet3])

            return bullets

        return []

    def power_up(self):
        """Increase player's power level"""
        self.power_level += 1
        if self.power_level > 3:
            self.power_level = 3

    def shield_up(self, amount=20):
        """Increase player's shield"""
        self.shield += amount
        if self.shield > self.max_shield:
            self.shield = self.max_shield

    def take_damage(self, damage):
        """Player takes damage"""
        self.shield -= damage
        if self.shield <= 0:
            self.lives -= 1
            self.shield = self.max_shield
            return True  # Player lost a life
        return False