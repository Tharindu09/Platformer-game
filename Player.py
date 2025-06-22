import pygame
from utils import load_sprite_sheets
class Player(pygame.sprite.Sprite):
    """
    Player character class with movement, jumping, and animation capabilities.
    """
    COLOR = (255, 0, 0)  # Red color (not used with sprites)
    GRAVITY = 1  # Gravity strength
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3  # Frames between animation updates

    def __init__(self, x, y, width, height):
        
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0  
        self.y_vel = 0  
        self.mask = None  # Collision mask
        self.direction = "left"  
        self.animation_count = 0  
        self.fall_count = 0  
        self.jump_count = 0 
        self.hit = False  
        self.hit_count = 0 
        self.health = 100 

    def jump(self):
        """Make the player jump (supports double jump)."""
        self.y_vel = -self.GRAVITY * 8  # Jump velocity
        self.animation_count = 0  # Reset animation
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0  # Reset fall count on first jump

    def move(self, dx, dy):
        """Move the player horizontally and vertically."""
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        """Trigger the hit state (when touching fire)."""
        self.hit = True

    def move_left(self, vel):
        
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0  # Reset animation when changing direction

    def move_right(self, vel):
        
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0  # Reset animation when changing direction

    def loop(self, fps,health_bar):
        
        # Apply gravity (increases over time for realistic acceleration)
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        # Move the player
        self.move(self.x_vel, self.y_vel)

        # Handle hit state timing
        if self.hit:
            self.hit_count += 1
        if self.hit_count > 2 :  # Hit state lasts 1 seconds
            self.health -= 20
            health_bar.update_health(self.health)
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        """Reset player state when landing on ground."""
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        """Handle player hitting ceiling."""
        self.count = 0
        self.y_vel *= -1  # Reverse vertical velocity

    def update_sprite(self):
        """Update the player's sprite based on current state."""
        sprite_sheet = "idle"  # Default animation
        
        # Choose animation based on player state
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:  # Moving upward
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:  # Falling fast
            sprite_sheet = "fall"
        elif self.x_vel != 0:  # Moving horizontally
            sprite_sheet = "run"

        # Get the appropriate sprite list
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        # Calculate current animation frame
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        """Update collision rect and mask based on current sprite."""
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        # Draw the player sprite
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
