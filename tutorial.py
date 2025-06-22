import pygame
from os import listdir
from os.path import isfile, join

# Initialize pygame
pygame.init()

# Set the window caption
pygame.display.set_caption("Platformer")

# Game constants
WIDTH, HEIGHT = 1000, 800  # Window dimensions
FPS = 60  # Frames per second
PLAYER_VEL = 5  # Player movement velocity

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))


def flip(sprites):
   
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """
    Load sprite sheets from a directory and split them into individual sprites.
    
    Args:
        dir1: First directory level (e.g., "MainCharacters")
        dir2: Second directory level (e.g., "MaskDude")
        width: Width of each sprite in the sheet
        height: Height of each sprite in the sheet
        direction: If True, create both left and right versions of sprites
    
    Returns:
        Dictionary mapping sprite names to lists of sprite surfaces
    """
    path = join("assets", dir1, dir2)
    # Get all image files in the directory
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        # Load the sprite sheet
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        # Split the sprite sheet into individual frames
        for i in range(sprite_sheet.get_width() // width):
            # Create a surface for each frame
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            # Scale the sprite 2x for better visibility
            sprites.append(pygame.transform.scale2x(surface))

        # Create directional sprites if needed
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    # Extract a specific block from the terrain sheet (at position 96, 0)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


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

    def loop(self, fps):
        
        # Apply gravity (increases over time for realistic acceleration)
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        # Move the player
        self.move(self.x_vel, self.y_vel)

        # Handle hit state timing
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:  # Hit state lasts 2 seconds
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


class Object(pygame.sprite.Sprite):
    """Base class for all game objects."""
    
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    """Solid block that player can stand on and collide with."""
    
    def __init__(self, x, y, size):
       
        super().__init__(x, y, size, size)
        # Load block sprite and create collision mask
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    """Animated fire trap that damages the player."""
    
    ANIMATION_DELAY = 3  # Frames between animation updates

    def __init__(self, x, y, width, height):
       
        super().__init__(x, y, width, height, "fire")
        # Load fire animation sprites
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]  # Start with fire off
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        # Calculate current animation frame
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        # Update collision rect and mask
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        # Reset animation counter when cycle completes
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name):
    """
    Create a tiled background from an image.
    
    Args:
        name: Background image filename
    
    Returns:
        Tuple of (tile_positions, background_image)
    """
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    # Calculate positions to tile the background across the screen
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    """
    Draw all game elements on screen.
    
    Args:
        window: Game window surface
        background: List of background tile positions
        bg_image: Background image
        player: Player object
        objects: List of game objects
        offset_x: Camera offset for scrolling
    """
    # Draw tiled background
    for tile in background:
        window.blit(bg_image, tile)

    # Draw all objects
    for obj in objects:
        obj.draw(window, offset_x)

    # Draw player
    player.draw(window, offset_x)

    # Update display
    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    """
    Handle collisions in the vertical direction (falling/jumping).
    
    Args:
        player: Player object
        objects: List of objects to check collision with
        dy: Vertical movement delta
    
    Returns:
        List of objects the player collided with
    """
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:  # Player is falling
                player.rect.bottom = obj.rect.top  # Place player on top of object
                player.landed()
            elif dy < 0:  # Player is jumping up
                player.rect.top = obj.rect.bottom  # Place player below object
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    """
    Check for horizontal collision without permanently moving the player.
    
    Args:
        player: Player object
        objects: List of objects to check collision with
        dx: Horizontal movement to test
    
    Returns:
        Object that would be collided with, or None
    """
    # Temporarily move player to test collision
    player.move(dx, 0)
    player.update()
    collided_object = None
    
    # Check for collision with any object
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    # Move player back to original position
    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    """
    Handle player movement input and collisions.
    
    Args:
        player: Player object
        objects: List of objects to check collision with
    """
    keys = pygame.key.get_pressed()

    # Reset horizontal velocity
    player.x_vel = 0
    
    # Check for potential collisions in both directions
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    # Move left if key pressed and no collision
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    # Move right if key pressed and no collision
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    # Handle vertical collisions
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    
    # Check all collided objects for special effects
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()  # Player takes damage from fire


def main(window):
   
    clock = pygame.time.Clock()
    
    # Load background
    background, bg_image = get_background("Blue.png")

    block_size = 96

    # Create game objects
    player = Player(100, 100, 50, 50)
    fire = Fire(200, HEIGHT - block_size - 64, 16, 32)
    fire.on()  # Turn on the fire
    
    # Create floor blocks across the screen
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    
    # Create additional platforms and add fire
    objects = [*floor, 
               Block(0, HEIGHT - block_size * 2, block_size),  # Left platform
               Block(block_size * 3, HEIGHT - block_size * 4, block_size),  # High platform
               fire]

    # Camera scrolling variables
    offset_x = 0  # Current camera offset
    scroll_area_width = 200  # Distance from edge before camera starts scrolling

    # Main game loop
    run = True
    while run:
        clock.tick(FPS)  # Maintain consistent framerate

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # Handle jump input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        # Update game objects
        player.loop(FPS)  # Update player physics and animation
        fire.loop()  # Update fire animation
        handle_move(player, objects)  # Handle player movement and collisions
        
        # Draw everything
        draw(window, background, bg_image, player, objects, offset_x)

        # Update camera scrolling
        # Scroll right when player approaches right edge
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel  # Move camera with player

    # Clean up
    pygame.quit()
    quit()


# Run the game if this file is executed directly
if __name__ == "__main__":
    main(window)