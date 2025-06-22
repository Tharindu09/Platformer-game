import pygame
from utils import load_sprite_sheets, get_block
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

class Item(Object):
    """Base class for collectable items."""
    
    def __init__(self, x, y, width, height, name=None):
        super().__init__(x, y, width, height, name)
        self.collected = False