import random

import pygame
import sys
from scripts.config import *
from scripts.utils import draw_text, create_button, load_ship_image

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.selected_ship = 'level1'
        self.ship_images = {
            'level1': load_ship_image('level1'),
            'level2': load_ship_image('level2'),
            'level3': load_ship_image('level3')
        }

        # Load background
        try:
            self.background = pygame.image.load(os.path.join(BACKGROUNDS_DIR, 'space_bg.png')).convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(DARK_BLUE)

            # Create some stars
            for _ in range(100):
                x = random.randrange(0, SCREEN_WIDTH)
                y = random.randrange(0, SCREEN_HEIGHT)
                size = random.randrange(1, 3)
                pygame.draw.circle(self.background, WHITE, (x, y), size)

        # Ship descriptions
        self.ship_descriptions = {
            'level1': "SCOUT - Fast and agile with standard firepower",
            'level2': "ASSAULT - Balanced speed with dual laser cannons",
            'level3': "DESTROYER - Heavy armor with triple laser spread"
        }

    def show_start_menu(self):
        """Display the main menu"""
        menu_running = True

        menu_music_path = os.path.join(SOUNDS_DIR, "menu_background.mp3")
        try:
            pygame.mixer.music.load(menu_music_path)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Menu music load error: {e}")

        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()  # Остановить музыку при выходе
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

            # Draw background
            self.screen.blit(self.background, (0, 0))

            # Draw title
            draw_text(self.screen, "GRADIUS EVOLUTION", 50, SCREEN_WIDTH // 2, 50, YELLOW)
            draw_text(self.screen, "Select your ship and start the mission", 25, SCREEN_WIDTH // 2, 120)

            # Create buttons
            start_action = create_button(
                "START GAME",
                SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                SCREEN_HEIGHT - 150,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                (50, 120, 50), (0, 200, 0),
                action="start"
            )
            exit_action = create_button(
                "EXIT",
                SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                SCREEN_HEIGHT - 80,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                (120, 50, 50), (200, 0, 0),
                action="exit"
            )

            if start_action:
                pygame.mixer.music.stop()
                return self.selected_ship

            if exit_action:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            # Draw ship selection
            self.draw_ship_selection()

            pygame.display.flip()

    def draw_ship_selection(self):
        """Draw ship selection interface"""
        ships = ['level1', 'level2', 'level3']
        center_y = SCREEN_HEIGHT // 2

        # Display each ship with selection indicators
        for i, ship_type in enumerate(ships):
            x_pos = 200 + i * 200

            # Draw selection box if this ship is selected
            if ship_type == self.selected_ship:
                pygame.draw.rect(self.screen, YELLOW,
                                 (x_pos - 60, center_y - 60, 120, 120), 3)

            # Draw ship image
            ship_img = self.ship_images.get(ship_type)
            ship_rect = ship_img.get_rect(center=(x_pos, center_y))
            self.screen.blit(ship_img, ship_rect)

            # Draw ship name and stats
            draw_text(self.screen, f"Ship {i + 1}", 20, x_pos, center_y + 70)

            # Create selection button
            select_action = create_button(
                "SELECT",
                x_pos - 50,
                center_y + 100,
                100, 30,
                (50, 50, 100), (80, 80, 160),
                action="select"
            )
            if select_action:
                self.selected_ship = ship_type

        # Draw ship description
        description = self.ship_descriptions.get(self.selected_ship, "")
        draw_text(self.screen, description, 18, SCREEN_WIDTH // 2, center_y + 160, WHITE)

        # Draw ship stats
        stats = SHIP_STATS.get(self.selected_ship, {})
        stat_y = center_y + 190
        draw_text(self.screen, f"Speed: {stats.get('speed', 0)}", 16, SCREEN_WIDTH // 2 - 100, stat_y)
        draw_text(self.screen, f"Fire Rate: {stats.get('fire_rate', 0)}", 16, SCREEN_WIDTH // 2, stat_y)
        draw_text(self.screen, f"Power: {stats.get('power', 0)}", 16, SCREEN_WIDTH // 2 + 100, stat_y)