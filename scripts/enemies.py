import pygame
import random
import math
from scripts.config import *
from scripts.utils import load_enemy_image, load_debris_image
from scripts.projectiles import EnemyBullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type="enemy1"):
        super().__init__()

        # Load enemy image based on type
        self.image = load_enemy_image(enemy_type)
        self.rect = self.image.get_rect()

        # Set enemy position off screen to the right
        self.rect.x = SCREEN_WIDTH + random.randrange(20, 100)
        self.rect.y = random.randrange(50, SCREEN_HEIGHT - 100)

        # Enemy attributes based on type
        if enemy_type == "enemy1":
            self.health = 20
            self.speed_min = ENEMY_SPEED_MIN
            self.speed_max = ENEMY_SPEED_MAX
            self.shoot_chance = ENEMY_SHOOT_CHANCE
            self.score_value = SCORE_ENEMY
            self.movement_pattern = "linear"
        elif enemy_type == "enemy2":
            self.health = 30
            self.speed_min = ENEMY_SPEED_MIN - 1
            self.speed_max = ENEMY_SPEED_MAX - 1
            self.shoot_chance = ENEMY_SHOOT_CHANCE * 1.5
            self.score_value = SCORE_ENEMY * 1.5
            self.movement_pattern = "sine"
        elif enemy_type == "enemy3":
            self.health = 50
            self.speed_min = ENEMY_SPEED_MIN - 2
            self.speed_max = ENEMY_SPEED_MAX - 2
            self.shoot_chance = ENEMY_SHOOT_CHANCE * 2
            self.score_value = SCORE_ENEMY * 2
            self.movement_pattern = "chase"

        # Set random speed
        self.speedx = -random.randrange(self.speed_min, self.speed_max)
        self.speedy = random.randrange(-2, 2)

        # Additional attributes for different movement patterns
        self.sine_amplitude = random.randrange(20, 40)
        self.sine_frequency = random.randrange(1, 3) * 0.01
        self.initial_y = self.rect.y
        self.angle = 0
        self.enemy_type = enemy_type
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randrange(1000, 3000)

    def update(self, player_x=None, player_y=None):
        # Move based on pattern
        self.rect.x += self.speedx

        if self.movement_pattern == "linear":
            self.rect.y += self.speedy

            # Bounce if hitting top or bottom
            if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
                self.speedy *= -1

        elif self.movement_pattern == "sine":
            # Sinusoidal movement
            self.angle += self.sine_frequency
            self.rect.y = self.initial_y + math.sin(self.angle) * self.sine_amplitude

        elif self.movement_pattern == "chase" and player_x is not None and player_y is not None:
            # Try to chase the player vertically
            if self.rect.centery < player_y:
                self.rect.y += 2
            elif self.rect.centery > player_y:
                self.rect.y -= 2

        # Respawn if off screen
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + random.randrange(20, 100)
            self.rect.y = random.randrange(50, SCREEN_HEIGHT - 100)
            self.speedx = -random.randrange(self.speed_min, self.speed_max)
            if self.movement_pattern == "linear":
                self.speedy = random.randrange(-2, 2)
            elif self.movement_pattern == "sine":
                self.initial_y = self.rect.y
                self.angle = 0

    def shoot(self, player_x=None, player_y=None):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot_delay = random.randrange(1000, 3000)

            # Type 3 enemies shoot homing bullets
            if self.enemy_type == "enemy3" and player_x is not None and player_y is not None:
                return EnemyBullet(self.rect.left, self.rect.centery, player_x, player_y)
            else:
                return EnemyBullet(self.rect.left, self.rect.centery)

        return None

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0


class Debris(pygame.sprite.Sprite):
    def __init__(self, debris_type="debris1"):
        super().__init__()

        # Load debris image
        self.image = load_debris_image(debris_type)
        self.rect = self.image.get_rect()

        # Set debris position off screen to the right
        self.rect.x = SCREEN_WIDTH + random.randrange(20, 100)
        self.rect.y = random.randrange(50, SCREEN_HEIGHT - 100)

        # Set random rotation and speed
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.original_image = self.image.copy()

        # Debris attributes
        self.health = 15
        self.speedx = -random.randrange(2, 5)
        self.speedy = random.randrange(-1, 1)
        self.score_value = SCORE_DEBRIS

    def update(self):
        # Move and rotate
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Rotate the debris
        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # Respawn if off screen
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + random.randrange(20, 100)
            self.rect.y = random.randrange(50, SCREEN_HEIGHT - 100)
            self.speedx = -random.randrange(2, 5)
            self.speedy = random.randrange(-1, 1)

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0