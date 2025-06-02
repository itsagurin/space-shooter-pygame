import os

# Game settings
TITLE = "Gradius Evolution"
SCREEN_WIDTH = 900  # было 800
SCREEN_HEIGHT = 700  # было 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
DARK_BLUE = (20, 30, 70)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

# Game difficulty settings
ENEMY_SPAWN_RATE = 3000  # milliseconds
DEBRIS_SPAWN_RATE = 2000  # milliseconds
POWERUP_CHANCE = 0.15  # 15% chance

# Player settings
PLAYER_SPEED = 5
PLAYER_LIVES = 3
PLAYER_SHOOT_DELAY = 250  # milliseconds

# Enemy settings
ENEMY_SPEED_MIN = 2
ENEMY_SPEED_MAX = 4
ENEMY_SHOOT_CHANCE = 0.008

# Ship unlock system
SHIP_UNLOCK_SCORES = {
    'level1': 0,      # Always unlocked
    'level2': 500,    # Unlocked at 500 points
    'level3': 1000    # Unlocked at 1000 points
}

# Ship characteristics
SHIP_STATS = {
    'level1': {
        'speed': 5,
        'fire_rate': 250,
        'power': 1,
        'health': 100
    },
    'level2': {
        'speed': 4,
        'fire_rate': 200,
        'power': 2,
        'health': 120
    },
    'level3': {
        'speed': 3,
        'fire_rate': 150,
        'power': 3,
        'health': 150
    }
}

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
FRIENDLY_SHIPS_DIR = os.path.join(IMAGE_DIR, "friendly_ships")
ENEMY_SHIPS_DIR = os.path.join(IMAGE_DIR, "enemy_ships")
SPACE_DEBRIS_DIR = os.path.join(IMAGE_DIR, "space_debris")
BACKGROUNDS_DIR = os.path.join(IMAGE_DIR, "backgrounds")
WEAPONS_DIR = os.path.join(IMAGE_DIR, "weapons")
POWERUPS_DIR = os.path.join(IMAGE_DIR, "powerups")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds")

# Score values
SCORE_ENEMY = 100
SCORE_DEBRIS = 25

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50