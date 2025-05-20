import pygame
from scripts.config import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color="blue", speed=10, speedy=0):
        super().__init__()

        # Load bullet image based on color
        filepath = os.path.join(WEAPONS_DIR, f"laser_{color}.png")
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            # Fallback if image not found
            self.image = pygame.Surface((10, 5))
            if color == "blue":
                self.image.fill(BLUE)
            elif color == "red":
                self.image.fill(RED)
            else:
                self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = speed
        self.speedy = speedy
        self.damage = 10

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Remove bullet if it goes off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x=None, target_y=None):
        super().__init__()

        # Load enemy bullet image
        filepath = os.path.join(WEAPONS_DIR, "laser_red.png")
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            # Fallback if image not found
            self.image = pygame.Surface((10, 5))
            self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y

        # Basic enemy bullet moves straight
        self.speedx = -7
        self.speedy = 0

        # Homing bullet if target is provided
        if target_x is not None and target_y is not None:
            dx = target_x - x
            dy = target_y - y
            mag = (dx ** 2 + dy ** 2) ** 0.5
            if mag > 0:  # Avoid division by zero
                self.speedx = (dx / mag) * 5
                self.speedy = (dy / mag) * 5

        self.damage = 10

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Remove bullet if it goes off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()