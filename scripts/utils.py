import pygame
from scripts.config import *


def load_image(filepath, scale=1.0):
    """Load an image and scale it if needed"""
    try:
        image = pygame.image.load(filepath)
        if scale != 1.0:
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image.convert_alpha()
    except pygame.error as e:
        print(f"Could not load image {filepath}: {e}")
        # Create a placeholder surface
        surface = pygame.Surface((50, 30))
        surface.fill(RED)
        return surface


def load_ship_image(ship_type):
    """Load a player ship image based on ship type and scale it down"""
    filepath = os.path.join(FRIENDLY_SHIPS_DIR, f"{ship_type}.png")
    img = pygame.image.load(filepath).convert_alpha()
    scale = 0.33
    new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
    img = pygame.transform.scale(img, new_size)
    return img


def load_enemy_image(enemy_type):
    """Load an enemy ship image based on enemy type and scale it down"""
    filepath = os.path.join(ENEMY_SHIPS_DIR, f"{enemy_type}.png")
    img = pygame.image.load(filepath).convert_alpha()
    scale = 0.33
    new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
    img = pygame.transform.scale(img, new_size)
    return img

def load_debris_image(debris_type):
    """Load a debris image based on debris type and scale it down"""
    filepath = os.path.join(SPACE_DEBRIS_DIR, f"{debris_type}.png")
    img = pygame.image.load(filepath).convert_alpha()
    scale = 0.33
    new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
    img = pygame.transform.scale(img, new_size)
    return img


def draw_text(surface, text, size, x, y, color=WHITE):
    """Draw text on the screen"""
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, pct):
    """Draw a shield bar on the screen"""
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


def draw_lives(surface, x, y, lives, image):
    """Draw player lives on the screen"""
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 35 * i
        img_rect.y = y
        surface.blit(image, img_rect)


def create_button(text, x, y, w, h, color, hover_color, action=None, events=None):
    import pygame
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont(None, 36)
    mouse = pygame.mouse.get_pos()
    click = False

    if events is None:
        events = pygame.event.get()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click and action is not None:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)
    return False