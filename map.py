from Object import Block, Fire

def create_challenging_map(WIDTH, HEIGHT, block_size):
    """
    Creates a challenging map with platforms, fires, and climbable blocks
    """
    # Create floor blocks across the screen
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    
    # Initialize objects list with floor
    objects = [*floor]
    
    # Add challenging platforms and obstacles
    platforms_and_obstacles = [
        # Starting area platforms
        Block(0, HEIGHT - block_size * 2, block_size),  # Left platform
        Block(block_size, HEIGHT - block_size * 2, block_size),
        Block(block_size * 3, HEIGHT - block_size * 3, block_size),
        
        # Climbing section - vertical blocks to climb
        Block(block_size * 5, HEIGHT - block_size * 2, block_size),
        Block(block_size * 5, HEIGHT - block_size * 3, block_size),
        Block(block_size * 5, HEIGHT - block_size * 4, block_size),
        Block(block_size * 5, HEIGHT - block_size * 5, block_size),
        
        # High platforms after climb
        Block(block_size * 6, HEIGHT - block_size * 5, block_size),
        Block(block_size * 7, HEIGHT - block_size * 5, block_size),
        Block(block_size * 8, HEIGHT - block_size * 5, block_size),
        
        # Floating platforms for jumping challenges
        Block(block_size * 10, HEIGHT - block_size * 3, block_size),
        Block(block_size * 12, HEIGHT - block_size * 4, block_size),
        Block(block_size * 14, HEIGHT - block_size * 2, block_size),
        
        # More climbing walls
        Block(block_size * 16, HEIGHT - block_size * 2, block_size),
        Block(block_size * 16, HEIGHT - block_size * 3, block_size),
        Block(block_size * 16, HEIGHT - block_size * 4, block_size),
        
        # Upper level platforms
        Block(block_size * 17, HEIGHT - block_size * 4, block_size),
        Block(block_size * 18, HEIGHT - block_size * 4, block_size),
        Block(block_size * 19, HEIGHT - block_size * 4, block_size),
        
        # Staircase section
        Block(block_size * 21, HEIGHT - block_size * 2, block_size),
        Block(block_size * 22, HEIGHT - block_size * 3, block_size),
        Block(block_size * 23, HEIGHT - block_size * 4, block_size),
        Block(block_size * 24, HEIGHT - block_size * 5, block_size),
        
        # Final platform
        Block(block_size * 25, HEIGHT - block_size * 5, block_size),
        Block(block_size * 26, HEIGHT - block_size * 5, block_size),
    ]
    
    # Add fire obstacles at strategic locations
    fires = [
        Fire(200, HEIGHT - block_size - 64, 16, 32),  # Original fire
        Fire(block_size * 3, HEIGHT - block_size - 64, 16, 32),  # Ground fire
        Fire(block_size * 9 - 50, HEIGHT - block_size * 6 +35, 16, 32),   # High fire
        Fire(block_size * 11, HEIGHT - block_size - 64, 16, 32), # Jump gap fire
        Fire(block_size * 15, HEIGHT - block_size - 64, 16, 32), # Before climb fire
        Fire(block_size * 20-30, HEIGHT - block_size * 5 +35, 16, 32),  # Upper level fire
    ]
    
    # Turn on all fires
    for fire in fires:
        fire.on()
    
    # Combine all objects
    objects.extend(platforms_and_obstacles)
    objects.extend(fires)
    
    return objects

def add_moving_platforms(objects, WIDTH, HEIGHT, block_size):
    """
    Optional: Add moving platforms for extra challenge
    (Requires MovingPlatform class implementation)
    """
    # Uncomment if you have MovingPlatform class
    # moving_platforms = [
    #     MovingPlatform(block_size * 13, HEIGHT - block_size * 3, block_size, 
    #                   block_size * 13, block_size * 15, speed=2),  # Horizontal moving
    #     MovingPlatform(block_size * 20, HEIGHT - block_size * 3, block_size,
    #                   HEIGHT - block_size * 3, HEIGHT - block_size * 5, speed=1, vertical=True)  # Vertical moving
    # ]
    # objects.extend(moving_platforms)
    pass

def create_enemy_spawn_points(WIDTH, HEIGHT, block_size):
    """
    Returns strategic positions for enemy spawning
    """
    enemy_spawns = [
        (block_size * 4, HEIGHT - block_size * 2),    # After first platform
        (block_size * 9, HEIGHT - block_size * 6),    # High platform
        (block_size * 13, HEIGHT - block_size - 32),  # Ground patrol
        (block_size * 20, HEIGHT - block_size * 5),   # Upper level
        (block_size * 25, HEIGHT - block_size * 6),   # Final area
    ]
    return enemy_spawns


