import random
import pygame
from scripts.config import *
from scripts.menu import Menu
from scripts.game import Game

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()  # Initialize sound mixer
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)


# Create required directories if they don't exist
def create_required_dirs():
    """Create necessary directories for the game"""
    directories = [
        os.path.join("images", "backgrounds"),
        os.path.join("images", "friendly_ships"),
        os.path.join("images", "enemy_ships"),
        os.path.join("images", "space_debris"),
        os.path.join("images", "weapons"),
        os.path.join("images", "powerups"),
        os.path.join("assets", "fonts"),
        os.path.join("assets", "sounds")
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def create_placeholder_images():
    """Create placeholder images if no images are available"""
    # Define placeholder images with their paths and colors
    placeholder_images = [
        # Ship images
        (os.path.join(FRIENDLY_SHIPS_DIR, "level1.png"), GREEN, (60, 40)),
        (os.path.join(FRIENDLY_SHIPS_DIR, "level2.png"), BLUE, (60, 40)),
        (os.path.join(FRIENDLY_SHIPS_DIR, "level3.png"), PURPLE, (60, 40)),

        # Enemy images
        (os.path.join(ENEMY_SHIPS_DIR, "enemy1.png"), RED, (50, 30)),
        (os.path.join(ENEMY_SHIPS_DIR, "enemy2.png"), (255, 100, 0), (50, 30)),
        (os.path.join(ENEMY_SHIPS_DIR, "enemy3.png"), (200, 0, 0), (60, 40)),

        # Debris images
        (os.path.join(SPACE_DEBRIS_DIR, "debris1.png"), (100, 100, 100), (30, 30)),
        (os.path.join(SPACE_DEBRIS_DIR, "debris2.png"), (150, 150, 100), (25, 25)),
        (os.path.join(SPACE_DEBRIS_DIR, "debris3.png"), (100, 100, 150), (35, 35)),

        # Weapon images
        (os.path.join(WEAPONS_DIR, "laser_blue.png"), BLUE, (20, 5)),
        (os.path.join(WEAPONS_DIR, "laser_red.png"), RED, (20, 5)),
        (os.path.join(WEAPONS_DIR, "laser_green.png"), GREEN, (20, 5)),

        # Power-up images
        (os.path.join(POWERUPS_DIR, "shield.png"), CYAN, (25, 25)),
        (os.path.join(POWERUPS_DIR, "power.png"), YELLOW, (25, 25)),
        (os.path.join(POWERUPS_DIR, "extra_life.png"), GREEN, (25, 25)),
        (os.path.join(POWERUPS_DIR, "speed.png"), BLUE, (25, 25)),

        # Background images
        (os.path.join(BACKGROUNDS_DIR, "space_bg.png"), DARK_BLUE, (SCREEN_WIDTH, SCREEN_HEIGHT)),
        (os.path.join(BACKGROUNDS_DIR, "nebula_bg.png"), (40, 0, 40), (SCREEN_WIDTH, SCREEN_HEIGHT))
    ]

    # Create each placeholder image if it doesn't exist
    for path, color, size in placeholder_images:
        if not os.path.exists(path):
            create_image(path, color, size)


def create_image(path, color, size):
    """Create and save a placeholder image"""
    surface = pygame.Surface(size)
    surface.fill(color)

    # For ship images, add some details
    if "ships" in path:
        # Draw a cockpit
        cockpit_color = (200, 200, 255)
        cockpit_width = size[0] // 3
        cockpit_height = size[1] // 2
        cockpit_x = size[0] // 2 - (cockpit_width // 2)
        cockpit_y = size[1] // 2 - (cockpit_height // 2)
        pygame.draw.ellipse(surface, cockpit_color, (cockpit_x, cockpit_y, cockpit_width, cockpit_height))

    # For debris, add some texture
    if "debris" in path:
        # Add random dots
        for _ in range(10):
            x = random.randrange(0, size[0])
            y = random.randrange(0, size[1])
            radius = random.randrange(1, 4)
            pygame.draw.circle(surface, (100, 100, 100), (x, y), radius)

    # For background images, add stars
    if "bg" in path:
        for _ in range(200):
            x = random.randrange(0, size[0])
            y = random.randrange(0, size[1])
            radius = random.randrange(1, 3)
            brightness = random.randrange(150, 256)
            pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), radius)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save the image
    pygame.image.save(surface, path)


def main():
    """Main function to run the game"""
    # Setup initial resources
    create_required_dirs()
    create_placeholder_images()

    # Start with the menu
    ship_type = None

    while True:
        menu = Menu(screen)
        ship_type = menu.show_start_menu()
        game = Game(screen, ship_type)
        score, high_score, exit_to_menu = game.run()
        if exit_to_menu:
            continue


if __name__ == "__main__":
    main()