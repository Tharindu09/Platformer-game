import pygame
from os import listdir
from os.path import isfile, join
import sys

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

def get_item(dir1,name):
    path = join("assets", "Items", dir1, name)
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
    surface.blit(image, (0, 0))
    return pygame.transform.scale2x(surface)

def draw(window, background, bg_image, player, objects, health_bar,offset_x):
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
    health_bar.draw(window)

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

def game_over(win, width, height,type, font_name="Arial", score=None):
    # Fill the screen with black
    win.fill((0, 0, 0))

    # Set up font
    font = pygame.font.SysFont(font_name, 64)
    text = font.render(type, True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    win.blit(text, text_rect)

    if score is not None:
        score_font = pygame.font.SysFont(font_name, 32)
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, height // 2 + 10))
        win.blit(score_text, score_rect)

    # Instruction to restart or quit
    info_font = pygame.font.SysFont(font_name, 24)
    info_text = info_font.render("Press R to Restart or Q to Quit", True, (200, 200, 200))
    info_rect = info_text.get_rect(center=(width // 2, height // 2 + 70))
    win.blit(info_text, info_rect)

    # Update the display
    pygame.display.flip()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    waiting = False  # Signal to restart

    return waiting