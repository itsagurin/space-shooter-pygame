import pygame
import random
from scripts.config import *


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, powerup_type=None):
        super().__init__()

        # Randomly choose power-up type if not specified
        if powerup_type is None:
            self.type = random.choice(['shield', 'power', 'extra_life', 'speed'])
        else:
            self.type = powerup_type

        # Load power-up image based on type
        filepath = os.path.join(POWERUPS_DIR, f"{self.type}.png")
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            # Fallback if image not found
            self.image = pygame.Surface((25, 25))
            if self.type == 'shield':
                self.image.fill(CYAN)
            elif self.type == 'power':
                self.image.fill(YELLOW)
            elif self.type == 'extra_life':
                self.image.fill(GREEN)
            elif self.type == 'speed':
                self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = -3
        self.speedy = random.choice([-1, 0, 1])

        # Add oscillation effect
        self.oscillate = True
        self.oscillate_amplitude = 5
        self.oscillate_speed = 0.1
        self.oscillate_counter = 0
        self.original_y = center[1]

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Add oscillation effect
        if self.oscillate:
            self.oscillate_counter += self.oscillate_speed
            self.rect.y = self.original_y + int(self.oscillate_amplitude *
                                                pygame.math.sin(self.oscillate_counter))

        # Remove power-up if it goes off screen
        if self.rect.right < 0:
            self.kill()

        # Keep power-up on screen vertically
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speedy *= -1