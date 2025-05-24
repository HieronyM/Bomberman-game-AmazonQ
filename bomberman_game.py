import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50
GRID_WIDTH = 15
GRID_HEIGHT = 11

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Set up the display
screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
pygame.display.set_caption('Bomberman Game')
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Game assets
def load_image(name, size=None):
    try:
        # Create more detailed representations using shapes instead of just colored rectangles
        image = pygame.Surface(size if size else (GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        if name == "player":
            # Create a more detailed Bomberman-like character
            # Body (white with blue outfit)
            pygame.draw.rect(image, (50, 100, 200), (GRID_SIZE//4, GRID_SIZE//2, GRID_SIZE//2, GRID_SIZE//2 - 5))  # Blue pants
            pygame.draw.circle(image, WHITE, (GRID_SIZE//2, GRID_SIZE//2 - 5), GRID_SIZE//3)  # White body/head
            pygame.draw.rect(image, (50, 100, 200), (GRID_SIZE//4, GRID_SIZE//2 - 5, GRID_SIZE//2, GRID_SIZE//6))  # Blue belt
            
            # Face details
            pygame.draw.circle(image, BLACK, (GRID_SIZE//2 - 5, GRID_SIZE//2 - 10), 3)  # Left eye
            pygame.draw.circle(image, BLACK, (GRID_SIZE//2 + 5, GRID_SIZE//2 - 10), 3)  # Right eye
            
            # Helmet/hat (white with blue band)
            pygame.draw.ellipse(image, WHITE, (GRID_SIZE//4, GRID_SIZE//6, GRID_SIZE//2, GRID_SIZE//3))  # White helmet
            pygame.draw.ellipse(image, (50, 100, 200), (GRID_SIZE//4, GRID_SIZE//4, GRID_SIZE//2, GRID_SIZE//8))  # Blue band
            
            # Arms
            pygame.draw.ellipse(image, WHITE, (GRID_SIZE//6, GRID_SIZE//2, GRID_SIZE//5, GRID_SIZE//3))  # Left arm
            pygame.draw.ellipse(image, WHITE, (GRID_SIZE*2//3, GRID_SIZE//2, GRID_SIZE//5, GRID_SIZE//3))  # Right arm
            
            # Feet
            pygame.draw.ellipse(image, (139, 69, 19), (GRID_SIZE//3, GRID_SIZE*3//4, GRID_SIZE//6, GRID_SIZE//6))  # Left foot
            pygame.draw.ellipse(image, (139, 69, 19), (GRID_SIZE//2, GRID_SIZE*3//4, GRID_SIZE//6, GRID_SIZE//6))  # Right foot
            
        elif name == "wall":
            # Create a brick wall pattern
            pygame.draw.rect(image, GRAY, (0, 0, GRID_SIZE, GRID_SIZE))
            # Add brick pattern
            for i in range(0, GRID_SIZE, 10):
                pygame.draw.line(image, BLACK, (0, i), (GRID_SIZE, i), 1)
            for i in range(0, GRID_SIZE, 10):
                pygame.draw.line(image, BLACK, (i, 0), (i, GRID_SIZE), 1)
                
        elif name == "block":
            # Create a wooden crate
            pygame.draw.rect(image, BROWN, (0, 0, GRID_SIZE, GRID_SIZE))
            # Add wood grain
            pygame.draw.line(image, (101, 67, 33), (5, 5), (GRID_SIZE-5, 5), 2)
            pygame.draw.line(image, (101, 67, 33), (5, GRID_SIZE//2), (GRID_SIZE-5, GRID_SIZE//2), 2)
            pygame.draw.line(image, (101, 67, 33), (5, GRID_SIZE-5), (GRID_SIZE-5, GRID_SIZE-5), 2)
            
        elif name == "bomb":
            # Create a round bomb with fuse
            pygame.draw.circle(image, BLACK, (GRID_SIZE//2, GRID_SIZE//2 + 5), GRID_SIZE//2 - 5)
            # Fuse
            pygame.draw.line(image, (139, 69, 19), (GRID_SIZE//2, 5), (GRID_SIZE//2, GRID_SIZE//2 - 5), 3)
            # Highlight
            pygame.draw.circle(image, WHITE, (GRID_SIZE//2 - 7, GRID_SIZE//2 - 7), 3)
            
        elif name == "explosion":
            # Create a star-like explosion
            pygame.draw.polygon(image, RED, [
                (GRID_SIZE//2, 0), 
                (GRID_SIZE//2 + 10, GRID_SIZE//2 - 10),
                (GRID_SIZE, GRID_SIZE//2),
                (GRID_SIZE//2 + 10, GRID_SIZE//2 + 10),
                (GRID_SIZE//2, GRID_SIZE),
                (GRID_SIZE//2 - 10, GRID_SIZE//2 + 10),
                (0, GRID_SIZE//2),
                (GRID_SIZE//2 - 10, GRID_SIZE//2 - 10)
            ])
            pygame.draw.circle(image, YELLOW, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//4)
            
        elif name == "powerup_bomb":
            # Improved bomb power-up
            # Background with gradient
            for y in range(GRID_SIZE):
                color_value = 50 + (y * 100 // GRID_SIZE)
                pygame.draw.line(image, (color_value, 0, 0), (0, y), (GRID_SIZE, y))
                
            # Border
            pygame.draw.rect(image, (200, 200, 200), (0, 0, GRID_SIZE, GRID_SIZE), 2)
            
            # Bomb icon
            pygame.draw.circle(image, BLACK, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//3)
            # Fuse
            pygame.draw.line(image, WHITE, (GRID_SIZE//2, GRID_SIZE//4), (GRID_SIZE//2, GRID_SIZE//3), 2)
            # Highlight
            pygame.draw.circle(image, WHITE, (GRID_SIZE//2 - 5, GRID_SIZE//2 - 5), 2)
            
            # +1 indicator
            text = small_font.render("+1", True, WHITE)
            text_rect = text.get_rect(center=(GRID_SIZE//2, GRID_SIZE*3//4))
            image.blit(text, text_rect)
            
        elif name == "powerup_range":
            # Improved range power-up
            # Background with gradient
            for y in range(GRID_SIZE):
                color_value = 50 + (y * 100 // GRID_SIZE)
                pygame.draw.line(image, (0, 0, color_value), (0, y), (GRID_SIZE, y))
                
            # Border
            pygame.draw.rect(image, (200, 200, 200), (0, 0, GRID_SIZE, GRID_SIZE), 2)
            
            # Flame icon
            flame_points = [
                (GRID_SIZE//2, GRID_SIZE//4),
                (GRID_SIZE//2 + GRID_SIZE//8, GRID_SIZE//2 - GRID_SIZE//8),
                (GRID_SIZE//2 + GRID_SIZE//6, GRID_SIZE//2),
                (GRID_SIZE//2 + GRID_SIZE//8, GRID_SIZE*5//8),
                (GRID_SIZE//2, GRID_SIZE*3//4),
                (GRID_SIZE//2 - GRID_SIZE//8, GRID_SIZE*5//8),
                (GRID_SIZE//2 - GRID_SIZE//6, GRID_SIZE//2),
                (GRID_SIZE//2 - GRID_SIZE//8, GRID_SIZE//2 - GRID_SIZE//8),
            ]
            pygame.draw.polygon(image, RED, flame_points)
            
            # Inner flame
            inner_flame_points = [
                (GRID_SIZE//2, GRID_SIZE//3),
                (GRID_SIZE//2 + GRID_SIZE//12, GRID_SIZE//2 - GRID_SIZE//12),
                (GRID_SIZE//2 + GRID_SIZE//10, GRID_SIZE//2),
                (GRID_SIZE//2 + GRID_SIZE//12, GRID_SIZE*9//16),
                (GRID_SIZE//2, GRID_SIZE*5//8),
                (GRID_SIZE//2 - GRID_SIZE//12, GRID_SIZE*9//16),
                (GRID_SIZE//2 - GRID_SIZE//10, GRID_SIZE//2),
                (GRID_SIZE//2 - GRID_SIZE//12, GRID_SIZE//2 - GRID_SIZE//12),
            ]
            pygame.draw.polygon(image, YELLOW, inner_flame_points)
            
            # +1 indicator
            text = small_font.render("+1", True, WHITE)
            text_rect = text.get_rect(center=(GRID_SIZE//2, GRID_SIZE*3//4))
            image.blit(text, text_rect)
            
        elif name == "powerup_speed":
            # Improved speed power-up
            # Background with gradient
            for y in range(GRID_SIZE):
                color_value = 50 + (y * 100 // GRID_SIZE)
                pygame.draw.line(image, (0, color_value, 0), (0, y), (GRID_SIZE, y))
                
            # Border
            pygame.draw.rect(image, (200, 200, 200), (0, 0, GRID_SIZE, GRID_SIZE), 2)
            
            # Speed icon (lightning bolt)
            bolt_points = [
                (GRID_SIZE//2 - GRID_SIZE//8, GRID_SIZE//4),
                (GRID_SIZE//2 + GRID_SIZE//4, GRID_SIZE//4),
                (GRID_SIZE//2, GRID_SIZE//2),
                (GRID_SIZE//2 + GRID_SIZE//8, GRID_SIZE//2),
                (GRID_SIZE//2 - GRID_SIZE//4, GRID_SIZE*3//4),
                (GRID_SIZE//2, GRID_SIZE//2 + GRID_SIZE//8),
                (GRID_SIZE//2 - GRID_SIZE//8, GRID_SIZE//2 + GRID_SIZE//8),
            ]
            pygame.draw.polygon(image, YELLOW, bolt_points)
            
            # Highlight
            pygame.draw.line(image, WHITE, 
                            (GRID_SIZE//2 - GRID_SIZE//8, GRID_SIZE//4), 
                            (GRID_SIZE//2 + GRID_SIZE//8, GRID_SIZE//4), 2)
            
            # +1 indicator
            text = small_font.render("+1", True, WHITE)
            text_rect = text.get_rect(center=(GRID_SIZE//2, GRID_SIZE*3//4))
            image.blit(text, text_rect)
            
        elif name == "enemy":
            # Create a more detailed enemy
            # Body
            pygame.draw.circle(image, PURPLE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2 - 5)
            # Eyes
            pygame.draw.circle(image, RED, (GRID_SIZE//2 - 7, GRID_SIZE//2 - 5), 4)
            pygame.draw.circle(image, RED, (GRID_SIZE//2 + 7, GRID_SIZE//2 - 5), 4)
            # Angry eyebrows
            pygame.draw.line(image, BLACK, (GRID_SIZE//2 - 12, GRID_SIZE//2 - 10), (GRID_SIZE//2 - 2, GRID_SIZE//2 - 7), 2)
            pygame.draw.line(image, BLACK, (GRID_SIZE//2 + 2, GRID_SIZE//2 - 7), (GRID_SIZE//2 + 12, GRID_SIZE//2 - 10), 2)
            # Mouth
            pygame.draw.arc(image, BLACK, (GRID_SIZE//2 - 10, GRID_SIZE//2 + 5, 20, 10), 3.14, 2*3.14, 2)
            
        return image
    except:
        # Fallback
        image = pygame.Surface(size if size else (GRID_SIZE, GRID_SIZE))
        image.fill(RED)
        return image

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1  # Fixed speed, no longer upgradable
        self.bomb_limit = 1
        self.bomb_range = 1
        self.bombs = []
        self.alive = True
        self.image = load_image("player")
        self.move_cooldown = 0  # Cooldown timer for movement
        self.move_cooldown_max = 10  # Frames to wait between moves
        
    def move(self, dx, dy, grid):
        # Only allow movement if cooldown is zero
        if self.move_cooldown > 0:
            return
            
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if the new position is valid
        if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
            grid[new_y][new_x] not in ["wall", "block", "bomb"]):
            self.x = new_x
            self.y = new_y
            
            # Set movement cooldown
            self.move_cooldown = self.move_cooldown_max
            
            # Check if player got a power-up
            if grid[new_y][new_x] is not None and grid[new_y][new_x].startswith("powerup"):
                self.collect_powerup(grid[new_y][new_x])
                grid[new_y][new_x] = None
    
    def update(self):
        # Update movement cooldown
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
    
    def place_bomb(self, grid):
        if len(self.bombs) < self.bomb_limit and grid[self.y][self.x] != "bomb":
            self.bombs.append(Bomb(self.x, self.y, self.bomb_range))
            grid[self.y][self.x] = "bomb"
            return True
        return False
    
    def collect_powerup(self, powerup_type):
        if powerup_type == "powerup_bomb":
            self.bomb_limit += 1
        elif powerup_type == "powerup_range":
            self.bomb_range += 1
        # Speed power-up removed
    
    def draw(self):
        screen.blit(self.image, (self.x * GRID_SIZE, self.y * GRID_SIZE))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.5
        self.move_counter = 0
        self.move_delay = 60  # Frames between moves
        self.alive = True
        self.image = load_image("enemy")
    
    def update(self, grid):
        if not self.alive:
            return
            
        self.move_counter += 1
        if self.move_counter >= self.move_delay:
            self.move_counter = 0
            
            # Simple AI: try to move in a random valid direction
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x = self.x + dx
                new_y = self.y + dy
                
                if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                    grid[new_y][new_x] not in ["wall", "block", "bomb", "enemy"]):
                    self.x = new_x
                    self.y = new_y
                    break
    
    def draw(self):
        if self.alive:
            screen.blit(self.image, (self.x * GRID_SIZE, self.y * GRID_SIZE))

class Bomb:
    def __init__(self, x, y, explosion_range):
        self.x = x
        self.y = y
        self.range = explosion_range
        self.timer = 180  # 3 seconds at 60 FPS
        self.exploded = False
        self.explosion_duration = 60  # 1 second at 60 FPS
        self.explosion_tiles = []
        self.image = load_image("bomb")
        self.explosion_image = load_image("explosion")
        self.animation_frame = 0  # For ticking animation
        self.animation_speed = 15  # Frames between animation changes
    
    def update(self, grid, blocks, enemies, player):
        if not self.exploded:
            self.timer -= 1
            
            # Update animation frame
            if self.timer % self.animation_speed == 0:
                self.animation_frame = (self.animation_frame + 1) % 4
                
            if self.timer <= 0:
                self.explode(grid, blocks, enemies, player)
        else:
            self.explosion_duration -= 1
            if self.explosion_duration <= 0:
                # Remove explosion tiles
                for x, y in self.explosion_tiles:
                    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] == "explosion":
                        grid[y][x] = None
                return True  # Bomb can be removed
        return False
    
    def explode(self, grid, blocks, enemies, player):
        self.exploded = True
        grid[self.y][self.x] = "explosion"
        self.explosion_tiles.append((self.x, self.y))
        
        # Explosion in four directions
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dx, dy = direction
            blocks_in_path = []  # Track blocks in this direction
            
            for r in range(1, self.range + 1):
                x = self.x + dx * r
                y = self.y + dy * r
                
                # Check if out of bounds
                if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
                    break
                
                # Check what's in the tile
                if grid[y][x] == "wall":
                    break  # Can't destroy walls
                elif grid[y][x] == "block":
                    # Add block to the list to be destroyed
                    blocks_in_path.append((x, y))
                    grid[y][x] = "explosion"
                    self.explosion_tiles.append((x, y))
                elif grid[y][x] == "bomb":
                    # Chain reaction - find the bomb and make it explode
                    for bomb in player.bombs:
                        if bomb.x == x and bomb.y == y and not bomb.exploded:
                            bomb.timer = 1  # Will explode next frame
                    grid[y][x] = "explosion"
                    self.explosion_tiles.append((x, y))
                else:
                    grid[y][x] = "explosion"
                    self.explosion_tiles.append((x, y))
                
                # Check if explosion hit enemies
                for enemy in enemies:
                    if enemy.x == x and enemy.y == y and enemy.alive:
                        enemy.alive = False
                
                # Check if explosion hit player
                if player.x == x and player.y == y and player.alive:
                    player.alive = False
            
            # Process all blocks in this direction after the explosion has passed through
            for x, y in blocks_in_path:
                if (x, y) in blocks:
                    blocks.remove((x, y))
                    
                    # 30% chance to spawn a power-up (only bomb or range now)
                    if random.random() < 0.3:
                        powerup_type = random.choice(["powerup_bomb", "powerup_range"])
                        grid[y][x] = powerup_type
    
    def draw(self):
        if not self.exploded:
            # Draw bomb with animation
            bomb_image = self.get_animated_bomb()
            screen.blit(bomb_image, (self.x * GRID_SIZE, self.y * GRID_SIZE))
        else:
            for x, y in self.explosion_tiles:
                # Get animated explosion based on position in explosion
                explosion_img = self.get_animated_explosion(x, y)
                screen.blit(explosion_img, (x * GRID_SIZE, y * GRID_SIZE))
    
    def get_animated_bomb(self):
        # Create a bomb with pulsing animation
        image = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Base bomb
        size_mod = 2 + self.animation_frame  # Makes the bomb "pulse"
        pygame.draw.circle(image, BLACK, (GRID_SIZE//2, GRID_SIZE//2 + 5), GRID_SIZE//2 - size_mod)
        
        # Fuse with animation
        fuse_color = (139, 69, 19) if self.animation_frame % 2 == 0 else (200, 100, 50)
        pygame.draw.line(image, fuse_color, (GRID_SIZE//2, 5), (GRID_SIZE//2, GRID_SIZE//2 - 5), 3)
        
        # Highlight
        pygame.draw.circle(image, WHITE, (GRID_SIZE//2 - 7, GRID_SIZE//2 - 7), 3)
        
        # Add a red blinking light when close to explosion
        if self.timer < 60:  # Last second
            if self.timer % 10 < 5:  # Blink every 5 frames
                pygame.draw.circle(image, RED, (GRID_SIZE//2 + 10, GRID_SIZE//2 - 10), 4)
        
        return image
    
    def get_animated_explosion(self, x, y):
        # Create explosion with animation based on position
        image = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Determine if this is center, edge, or corner of explosion
        is_center = (x == self.x and y == self.y)
        
        if is_center:
            # Center explosion (bigger)
            pygame.draw.circle(image, ORANGE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
            pygame.draw.circle(image, YELLOW, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//3)
        else:
            # Directional explosion
            # Determine direction from center
            dx = x - self.x
            dy = y - self.y
            
            if dx != 0 and dy == 0:  # Horizontal
                pygame.draw.ellipse(image, RED, (0, GRID_SIZE//4, GRID_SIZE, GRID_SIZE//2))
                pygame.draw.ellipse(image, ORANGE, (GRID_SIZE//4, GRID_SIZE//3, GRID_SIZE//2, GRID_SIZE//3))
            elif dx == 0 and dy != 0:  # Vertical
                pygame.draw.ellipse(image, RED, (GRID_SIZE//4, 0, GRID_SIZE//2, GRID_SIZE))
                pygame.draw.ellipse(image, ORANGE, (GRID_SIZE//3, GRID_SIZE//4, GRID_SIZE//3, GRID_SIZE//2))
        
        # Add flickering effect
        if random.random() < 0.3:
            # Random sparks
            for _ in range(3):
                spark_x = random.randint(GRID_SIZE//4, GRID_SIZE*3//4)
                spark_y = random.randint(GRID_SIZE//4, GRID_SIZE*3//4)
                spark_size = random.randint(2, 5)
                pygame.draw.circle(image, WHITE, (spark_x, spark_y), spark_size)
        
        return image

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        
        # Draw button with rounded corners and gradient
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        # Add a highlight effect at the top
        highlight_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height // 3)
        pygame.draw.rect(screen, (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50)), 
                        highlight_rect, border_radius=10)
        
        # Add a shadow effect
        pygame.draw.rect(screen, (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50)), 
                        self.rect, 2, border_radius=10)
        
        # Draw text with slight shadow for better readability
        text_surface = font.render(self.text, True, WHITE)
        text_shadow = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Draw shadow slightly offset
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(text_shadow, shadow_rect)
        
        # Draw main text
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

def generate_level():
    # Create empty grid
    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    blocks = []
    
    # Add walls (border and checkerboard pattern)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            # Border walls
            if x == 0 or y == 0 or x == GRID_WIDTH - 1 or y == GRID_HEIGHT - 1:
                grid[y][x] = "wall"
            # Checkerboard walls
            elif x % 2 == 0 and y % 2 == 0:
                grid[y][x] = "wall"
    
    # Add destructible blocks (50% chance in empty spaces)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] is None and random.random() < 0.5:
                # Keep the starting area clear
                if not (x < 3 and y < 3):
                    grid[y][x] = "block"
                    blocks.append((x, y))
    
    return grid, blocks

def spawn_enemies(grid, num_enemies):
    enemies = []
    for _ in range(num_enemies):
        # Find a random empty spot
        while True:
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
            
            # Don't spawn too close to player
            if (x < 3 and y < 3) or grid[y][x] is not None:
                continue
                
            enemies.append(Enemy(x, y))
            grid[y][x] = "enemy"
            break
    
    return enemies

def draw_grid(grid):
    # Draw a grass-like background
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Alternating pattern for grass
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, (50, 120, 50), rect)  # Darker green
            else:
                pygame.draw.rect(screen, (70, 140, 70), rect)  # Lighter green
            
            # Draw grid elements
            if grid[y][x] == "wall":
                screen.blit(load_image("wall"), (x * GRID_SIZE, y * GRID_SIZE))
            elif grid[y][x] == "block":
                screen.blit(load_image("block"), (x * GRID_SIZE, y * GRID_SIZE))
            elif grid[y][x] == "bomb":
                pass  # Bombs are drawn separately
            elif grid[y][x] == "explosion":
                screen.blit(load_image("explosion"), (x * GRID_SIZE, y * GRID_SIZE))
            elif grid[y][x] == "powerup_bomb":
                screen.blit(load_image("powerup_bomb"), (x * GRID_SIZE, y * GRID_SIZE))
            elif grid[y][x] == "powerup_range":
                screen.blit(load_image("powerup_range"), (x * GRID_SIZE, y * GRID_SIZE))
            elif grid[y][x] == "powerup_speed":
                screen.blit(load_image("powerup_speed"), (x * GRID_SIZE, y * GRID_SIZE))

def draw_hud(player, level):
    # Draw HUD background with gradient
    hud_height = 50
    hud_rect = pygame.Rect(0, GRID_HEIGHT * GRID_SIZE - hud_height, GRID_WIDTH * GRID_SIZE, hud_height)
    
    # Draw gradient background
    for i in range(hud_height):
        color_value = 40 + i
        pygame.draw.line(screen, (color_value, color_value, color_value), 
                        (0, GRID_HEIGHT * GRID_SIZE - hud_height + i), 
                        (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE - hud_height + i))
    
    pygame.draw.rect(screen, WHITE, hud_rect, 2)
    
    # Draw player stats with improved icons
    # Bomb stat with improved icon
    bomb_icon_size = 30
    bomb_icon_y = GRID_HEIGHT * GRID_SIZE - 40
    
    # Draw bomb icon background (circle)
    pygame.draw.circle(screen, BLACK, (30, bomb_icon_y + bomb_icon_size//2), bomb_icon_size//2)
    # Draw fuse
    pygame.draw.line(screen, (139, 69, 19), (30, bomb_icon_y + 5), (30, bomb_icon_y + bomb_icon_size//2 - 5), 3)
    # Highlight
    pygame.draw.circle(screen, WHITE, (25, bomb_icon_y + bomb_icon_size//2 - 5), 3)
    
    # Draw bomb count with larger font and better positioning
    bomb_text = font.render(f"x{player.bomb_limit}", True, WHITE)
    screen.blit(bomb_text, (50, bomb_icon_y + 5))
    
    # Range stat with improved icon
    range_icon_x = 120
    
    # Draw flame icon
    flame_color = RED
    flame_points = [
        (range_icon_x, bomb_icon_y + 5),
        (range_icon_x + 10, bomb_icon_y + 15),
        (range_icon_x + 5, bomb_icon_y + 12),
        (range_icon_x + 15, bomb_icon_y + 25),
        (range_icon_x, bomb_icon_y + 20),
        (range_icon_x - 15, bomb_icon_y + 25),
        (range_icon_x - 5, bomb_icon_y + 12),
        (range_icon_x - 10, bomb_icon_y + 15),
    ]
    pygame.draw.polygon(screen, flame_color, flame_points)
    
    # Inner flame
    inner_flame_color = YELLOW
    inner_flame_points = [
        (range_icon_x, bomb_icon_y + 8),
        (range_icon_x + 6, bomb_icon_y + 15),
        (range_icon_x + 3, bomb_icon_y + 13),
        (range_icon_x + 8, bomb_icon_y + 22),
        (range_icon_x, bomb_icon_y + 18),
        (range_icon_x - 8, bomb_icon_y + 22),
        (range_icon_x - 3, bomb_icon_y + 13),
        (range_icon_x - 6, bomb_icon_y + 15),
    ]
    pygame.draw.polygon(screen, inner_flame_color, inner_flame_points)
    
    # Draw range count with larger font and better positioning
    range_text = font.render(f"x{player.bomb_range}", True, WHITE)
    screen.blit(range_text, (range_icon_x + 25, bomb_icon_y + 5))
    
    # Level indicator with improved styling
    level_text = font.render(f"Level: {level}", True, YELLOW)
    screen.blit(level_text, (GRID_WIDTH * GRID_SIZE - 150, GRID_HEIGHT * GRID_SIZE - 40))

def main():
    # Game states
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    LEVEL_COMPLETE = 3
    
    game_state = MENU
    level = 1
    
    # Create buttons with better styling
    button_width = 200
    button_height = 50
    
    start_button = Button(GRID_WIDTH * GRID_SIZE // 2 - button_width // 2, 
                         GRID_HEIGHT * GRID_SIZE // 2, 
                         button_width, button_height, 
                         "Start Game", (0, 100, 200), (0, 150, 255))
    
    next_level_button = Button(GRID_WIDTH * GRID_SIZE // 2 - button_width // 2, 
                              GRID_HEIGHT * GRID_SIZE // 2, 
                              button_width, button_height, 
                              "Next Level", (0, 150, 0), (0, 200, 0))
    
    play_again_button = Button(GRID_WIDTH * GRID_SIZE // 2 - button_width // 2, 
                              GRID_HEIGHT * GRID_SIZE // 2, 
                              button_width, button_height, 
                              "Play Again", (0, 100, 200), (0, 150, 255))
    
    # Game variables
    grid = None
    blocks = None
    player = None
    enemies = None
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_clicked = True
            elif event.type == pygame.KEYDOWN:
                if game_state == PLAYING:
                    if event.key == pygame.K_SPACE:
                        player.place_bomb(grid)
        
        if game_state == MENU:
            # Draw menu
            screen.fill(BLACK)
            title = font.render("BOMBERMAN", True, WHITE)
            screen.blit(title, (GRID_WIDTH * GRID_SIZE // 2 - title.get_width() // 2, 
                               GRID_HEIGHT * GRID_SIZE // 4))
            
            # Draw instructions
            instructions = [
                "Arrow keys to move",
                "Space to place bombs",
                "Destroy blocks to find power-ups",
                "Eliminate all enemies to complete the level"
            ]
            
            for i, line in enumerate(instructions):
                instr_text = small_font.render(line, True, WHITE)
                screen.blit(instr_text, (GRID_WIDTH * GRID_SIZE // 2 - instr_text.get_width() // 2, 
                                        GRID_HEIGHT * GRID_SIZE // 3 + i * 30))
            
            # Draw and handle start button
            start_button.check_hover(mouse_pos)
            start_button.draw()
            
            if start_button.is_clicked(mouse_pos, mouse_clicked):
                # Initialize game
                grid, blocks = generate_level()
                player = Player(1, 1)
                
                # Calculate number of enemies based on level
                num_enemies = 3 + level  # Base of 3 enemies + current level
                if level > 5:
                    num_enemies += level - 5  # Even more enemies after level 5
                    
                enemies = spawn_enemies(grid, num_enemies)
                game_state = PLAYING
        
        elif game_state == PLAYING:
            # Update player
            player.update()
            
            # Handle player movement on key press (not continuous)
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP]:
                player.move(0, -1, grid)
            elif keys_pressed[pygame.K_DOWN]:
                player.move(0, 1, grid)
            elif keys_pressed[pygame.K_LEFT]:
                player.move(-1, 0, grid)
            elif keys_pressed[pygame.K_RIGHT]:
                player.move(1, 0, grid)
            
            # Update bombs
            for bomb in player.bombs[:]:
                if bomb.update(grid, blocks, enemies, player):
                    player.bombs.remove(bomb)
                    if grid[bomb.y][bomb.x] == "explosion":
                        grid[bomb.y][bomb.x] = None
            
            # Update enemies
            for enemy in enemies:
                enemy.update(grid)
                
                # Check if enemy caught player
                if enemy.x == player.x and enemy.y == player.y and enemy.alive and player.alive:
                    player.alive = False
            
            # Check if player is in explosion
            if grid[player.y][player.x] == "explosion" and player.alive:
                player.alive = False
            
            # Check game over condition
            if not player.alive:
                game_state = GAME_OVER
            
            # Check level complete condition
            alive_enemies = sum(1 for enemy in enemies if enemy.alive)
            if alive_enemies == 0:
                game_state = LEVEL_COMPLETE
            
            # Draw everything
            draw_grid(grid)
            
            # Draw bombs
            for bomb in player.bombs:
                bomb.draw()
            
            # Draw enemies
            for enemy in enemies:
                enemy.draw()
            
            # Draw player
            player.draw()
            
            # Draw HUD
            draw_hud(player, level)
        
        elif game_state == LEVEL_COMPLETE:
            # Draw level complete screen
            screen.fill(BLACK)
            
            complete_text = font.render(f"Level {level} Complete!", True, GREEN)
            screen.blit(complete_text, (GRID_WIDTH * GRID_SIZE // 2 - complete_text.get_width() // 2, 
                                      GRID_HEIGHT * GRID_SIZE // 3))
            
            # Draw and handle next level button
            next_level_button.check_hover(mouse_pos)
            next_level_button.draw()
            
            if next_level_button.is_clicked(mouse_pos, mouse_clicked):
                # Go to next level
                level += 1
                grid, blocks = generate_level()
                
                # Reset player stats and position
                player.x = 1
                player.y = 1
                player.bombs = []
                player.bomb_limit = 1  # Reset bomb limit to initial value
                player.bomb_range = 1  # Reset bomb range to initial value
                
                # Increase number of enemies based on level
                # More enemies in higher levels with progressive scaling
                num_enemies = 3 + level  # Base of 3 enemies + current level
                if level > 5:
                    num_enemies += level - 5  # Even more enemies after level 5
                
                enemies = spawn_enemies(grid, num_enemies)
                game_state = PLAYING
        
        elif game_state == GAME_OVER:
            # Draw game over screen
            screen.fill(BLACK)
            
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (GRID_WIDTH * GRID_SIZE // 2 - game_over_text.get_width() // 2, 
                                       GRID_HEIGHT * GRID_SIZE // 3))
            
            level_text = font.render(f"You reached level {level}", True, WHITE)
            screen.blit(level_text, (GRID_WIDTH * GRID_SIZE // 2 - level_text.get_width() // 2, 
                                   GRID_HEIGHT * GRID_SIZE // 3 + 50))
            
            # Draw and handle play again button
            play_again_button.check_hover(mouse_pos)
            play_again_button.draw()
            
            if play_again_button.is_clicked(mouse_pos, mouse_clicked):
                # Reset game
                level = 1
                game_state = MENU
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
