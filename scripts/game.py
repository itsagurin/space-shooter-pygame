import pygame
import random
import sys
import os
from scripts.config import *
from scripts.player import Player
from scripts.enemies import Enemy, Debris
from scripts.powerups import PowerUp
from scripts.utils import draw_text, draw_shield_bar, draw_lives, create_button

class Game:
    def __init__(self, screen, ship_type='level1'):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.ship_type = ship_type
        self.running = True
        self.paused = False
        self.game_over = False
        self.score = 0
        self.level = 1
        self.spawn_rate_multiplier = 1.0

        # Load game background
        try:
            self.background = pygame.image.load(os.path.join(BACKGROUNDS_DIR, 'nebula_bg.png')).convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(DARK_BLUE)

            # Create stars
            for _ in range(200):
                x = random.randrange(0, SCREEN_WIDTH)
                y = random.randrange(0, SCREEN_HEIGHT)
                size = random.randrange(1, 3)
                color = random.choice([WHITE, (200, 200, 255), (255, 200, 200)])
                pygame.draw.circle(self.background, color, (x, y), size)

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.debris = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # Create player
        self.player = Player(ship_type)
        self.all_sprites.add(self.player)
        self.player_group.add(self.player)

        # --- Dynamic spawn control ---
        self.enemy_max_count = 2
        self.debris_max_count = 1
        self.enemy_increase_interval = 30000
        self.debris_increase_interval = 60000
        self.last_enemy_count_increase = pygame.time.get_ticks()
        self.last_debris_count_increase = pygame.time.get_ticks()

        # Set timers for spawning entities
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.last_debris_spawn = pygame.time.get_ticks()
        self.level_up_time = pygame.time.get_ticks()

        # Initial enemy and debris spawning
        self.spawn_enemies(self.enemy_max_count)
        self.spawn_debris(self.debris_max_count)

        # Score and level progression
        self.high_score = 0
        self.try_load_high_score()

        # --------- ДОБАВЛЕНО: Загрузка звука выстрела игрока ---------
        self.shot_sound = None
        shot_path = os.path.join(SOUNDS_DIR, "shot.wav")
        if os.path.exists(shot_path):
            try:
                self.shot_sound = pygame.mixer.Sound(shot_path)
                self.shot_sound.set_volume(0.5)  # Громкость по желанию
            except Exception as e:
                print(f"Could not load shot.wav: {e}")
        # -------------------------------------------------------------

    def run(self):
        """Main game loop"""
        exit_to_menu = False
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()

            if not self.paused and not self.game_over:
                self.update()
            self.draw()

            if self.game_over:
                result = self.draw_game_over_screen()
                if result == "menu":
                    exit_to_menu = True
                    self.running = False
                elif result == "restart":
                    self.__init__(self.screen, self.ship_type)

        return self.score, self.high_score, exit_to_menu

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_SPACE and not self.paused:
                    self.fire_player_weapon()

            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.screen, self.ship_type)
                    if event.key == pygame.K_m:
                        self.running = False

    def update(self):
        """Update game state"""
        now = pygame.time.get_ticks()

        # Увеличение максимального количества врагов и debris каждую минуту
        if now - self.last_enemy_count_increase > self.enemy_increase_interval:
            self.enemy_max_count += 1
            self.last_enemy_count_increase = now

        if now - self.last_debris_count_increase > self.debris_increase_interval:
            self.debris_max_count += 1
            self.last_debris_count_increase = now

        # Поддерживаем нужное количество врагов и debris на экране
        if len(self.enemies) < self.enemy_max_count:
            self.spawn_enemies(self.enemy_max_count - len(self.enemies))
        if len(self.debris) < self.debris_max_count:
            self.spawn_debris(self.debris_max_count - len(self.debris))

        # Check for level up
        if now - self.level_up_time > 30000:  # Level up every 30 seconds
            self.level_up()
            self.level_up_time = now

        # Update all sprites
        self.all_sprites.update()

        # Update enemies with player position for targeting
        for enemy in self.enemies:
            enemy.update(self.player.rect.centerx, self.player.rect.centery)
            # Enemy shooting
            if random.random() < enemy.shoot_chance:
                bullet = enemy.shoot(self.player.rect.centerx, self.player.rect.centery)
                if bullet:
                    self.all_sprites.add(bullet)
                    self.enemy_bullets.add(bullet)

        # Spawn new enemies (по таймеру, но не превышаем лимит)
        if now - self.last_enemy_spawn > ENEMY_SPAWN_RATE / self.spawn_rate_multiplier:
            self.last_enemy_spawn = now
            if len(self.enemies) < self.enemy_max_count:
                self.spawn_enemies(1)

        # Spawn new debris (по таймеру, но не превышаем лимит)
        if now - self.last_debris_spawn > DEBRIS_SPAWN_RATE / self.spawn_rate_multiplier:
            self.last_debris_spawn = now
            if len(self.debris) < self.debris_max_count:
                self.spawn_debris(1)

        # Check for collisions
        self.check_collisions()

        # Check for game over
        if self.player.lives <= 0 and not self.game_over:
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

    def draw(self):
        """Draw the game screen"""
        self.screen.blit(self.background, (0, 0))

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # Draw HUD
        self.draw_hud()

        # Draw pause screen
        if self.paused:
            self.draw_pause_screen()

        # Draw game over screen
        if self.game_over:
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_hud(self):
        """Draw heads-up display"""
        # Score
        draw_text(self.screen, f"Score: {self.score}", 22, 100, 20, WHITE)
        draw_text(self.screen, f"High Score: {self.high_score}", 18, 100, 50, WHITE)

        # Shield bar
        draw_shield_bar(self.screen, 10, 20, self.player.shield)

        # Lives
        draw_text(self.screen, "Lives:", 18, SCREEN_WIDTH - 100, 10, WHITE)
        draw_lives(self.screen, SCREEN_WIDTH - 100, 35, self.player.lives, self.player.mini_ship)

        # Level
        draw_text(self.screen, f"Level: {self.level}", 18, SCREEN_WIDTH // 2, 20, WHITE)

        # Power level
        draw_text(self.screen, f"Power: {self.player.power_level}", 18, SCREEN_WIDTH // 2 - 100, 20, YELLOW)

    def draw_pause_screen(self):
        """Draw pause screen overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, "PAUSED", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, WHITE)
        draw_text(self.screen, "Press P to continue", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, WHITE)

    def draw_game_over_screen(self):
        """Draw game over screen overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, RED)
        draw_text(self.screen, f"Final Score: {self.score}", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)

        restart_action = create_button("RESTART", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80,
                                       200, 40, (50, 120, 50), (0, 200, 0), action="restart")
        menu_action = create_button("MAIN MENU", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140,
                                    200, 40, (120, 50, 50), (200, 0, 0), action="menu")

        pygame.display.flip()

        if restart_action:
            return "restart"
        if menu_action:
            return "menu"
        return None

    def spawn_enemies(self, count):
        """Spawn new enemies"""
        enemy_types = ["enemy1", "enemy2", "enemy3"]
        weights = [0.6, 0.3, 0.1]  # Spawn probabilities, should sum to 1

        # Adjust weights based on level
        if self.level >= 3:
            weights = [0.5, 0.3, 0.2]
        if self.level >= 5:
            weights = [0.4, 0.4, 0.2]
        if self.level >= 8:
            weights = [0.3, 0.4, 0.3]

        for _ in range(count):
            enemy_type = random.choices(enemy_types, weights=weights)[0]
            enemy = Enemy(enemy_type)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def spawn_debris(self, count):
        """Spawn new debris"""
        debris_types = ["debris1", "debris2", "debris3"]

        for _ in range(count):
            debris_type = random.choice(debris_types)
            debris = Debris(debris_type)
            self.all_sprites.add(debris)
            self.debris.add(debris)

    def fire_player_weapon(self):
        """Fire player's weapon"""
        bullets = self.player.shoot()
        if bullets and self.shot_sound:
            self.shot_sound.play()
        for bullet in bullets:
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)

    def check_collisions(self):
        """Check for all game collisions"""
        # Bullets hitting enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullet_list in hits.items():
            for _ in bullet_list:
                if enemy.take_damage(10):
                    self.score += int(enemy.score_value)
                    enemy.kill()

                    # Chance to spawn powerup
                    if random.random() < POWERUP_CHANCE:
                        powerup = PowerUp(enemy.rect.center)
                        self.all_sprites.add(powerup)
                        self.powerups.add(powerup)

        # Bullets hitting debris
        hits = pygame.sprite.groupcollide(self.debris, self.bullets, False, True)
        for debris, bullet_list in hits.items():
            for _ in bullet_list:
                if debris.take_damage(10):
                    self.score += int(debris.score_value)
                    debris.kill()

        # Player colliding with enemies
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for hit in hits:
            self.spawn_enemies(1)  # Respawn enemy
            if self.player.take_damage(25):
                self.check_game_over()

        # Player colliding with debris
        hits = pygame.sprite.spritecollide(self.player, self.debris, True)
        for hit in hits:
            self.spawn_debris(1)  # Respawn debris
            if self.player.take_damage(15):
                self.check_game_over()

        # Player hit by enemy bullets
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for hit in hits:
            if self.player.take_damage(10):
                self.check_game_over()

        # Player collecting powerups
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                self.player.shield_up(20)
            elif hit.type == 'power':
                self.player.power_up()
            elif hit.type == 'extra_life':
                self.player.lives += 1
            elif hit.type == 'speed':
                self.player.speed += 1

    def check_game_over(self):
        """Check if player has lost all lives"""
        if self.player.lives <= 0:
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

    def level_up(self):
        """Increase game difficulty"""
        self.level += 1
        self.spawn_rate_multiplier += 0.2

        # Spawn extra enemies on level up
        if self.level % 2 == 0:
            self.spawn_enemies(2)

        # Power up player occasionally
        if self.level % 3 == 0 and self.player.power_level < 3:
            self.player.power_up()

    def try_load_high_score(self):
        """Try to load high score from a file"""
        try:
            with open('highscore.txt', 'r') as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0

    def save_high_score(self):
        """Save high score to a file"""
        try:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))
        except:
            pass