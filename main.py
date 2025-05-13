import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gradius Clone")
clock = pygame.time.Clock()


# Загрузка изображений
def load_image(name, scale=1):
    # Это заглушка, в реальном проекте стоит использовать изображения
    surface = pygame.Surface((50, 30))
    if name == "ship":
        surface.fill(GREEN)
    elif name == "enemy":
        surface.fill(RED)
    elif name == "laser":
        surface = pygame.Surface((10, 5))
        surface.fill(BLUE)
    return surface


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("ship")
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = SCREEN_HEIGHT // 2
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 250  # миллисекунды
        self.last_shot = pygame.time.get_ticks()
        self.power_level = 1
        self.lives = 3

    def update(self):
        # Движение с клавиатуры
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8

        # Обновление позиции
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Ограничение экрана
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power_level == 1:
                bullet = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.power_level >= 2:
                bullet1 = Bullet(self.rect.right, self.rect.centery - 10)
                bullet2 = Bullet(self.rect.right, self.rect.centery + 10)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("enemy")
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + 20
        self.rect.y = random.randrange(50, SCREEN_HEIGHT - 100)
        self.speedx = random.randrange(-9, -3)
        self.speedy = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Если враг улетел за экран - респаун
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + 20
            self.rect.y = random.randrange(50, SCREEN_HEIGHT - 100)
            self.speedx = random.randrange(-9, -3)
            self.speedy = random.randrange(-2, 2)

        # Держим врагов в пределах экрана по вертикали
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speedy *= -1


# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("laser")
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        # Удаление пули, если она улетела за экран
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


# Класс улучшения
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(['shield', 'power'])
        self.image = pygame.Surface((25, 25))
        if self.type == 'shield':
            self.image.fill((0, 255, 255))  # Голубой для щита
        else:
            self.image.fill((255, 255, 0))  # Желтый для усиления
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = -3

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()


# Отображение счета и жизней
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# Функция создания нового врага
def new_enemy():
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)


# Инициализация спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Создание группы врагов
for i in range(8):
    new_enemy()

# Счет игры
score = 0
shield = 100

# Основной игровой цикл
running = True
while running:
    # Поддержание правильной скорости игры
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False

    # Обновление состояния
    all_sprites.update()

    # Проверка столкновения пуль и врагов
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius // 2
        if random.random() > 0.9:
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        new_enemy()

    # Проверка столкновения игрока и врагов
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        shield -= 25
        new_enemy()
        if shield <= 0:
            player.lives -= 1
            shield = 100
            if player.lives == 0:
                running = False

    # Проверка столкновения игрока и улучшений
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            shield += 20
            if shield > 100:
                shield = 100
        if hit.type == 'power':
            player.power_level += 1

    # Отрисовка
    screen.fill(BLACK)

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)

    # Отрисовка счета и здоровья
    draw_text(screen, f"Счет: {score}", 18, SCREEN_WIDTH // 2, 10)
    draw_shield_bar(screen, 5, 5, shield)
    draw_lives(screen, SCREEN_WIDTH - 100, 5, player.lives, load_image("ship", 0.5))

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
sys.exit()