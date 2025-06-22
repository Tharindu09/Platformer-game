import pygame
from utils import get_background,handle_move,draw,game_over
from map import create_challenging_map
from Player import Player
from Object import  Fire
from HealthBar import HealthBar

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


def main(window):
   
    clock = pygame.time.Clock()
    
    # Load background
    background, bg_image = get_background("Blue.png")

    block_size = 96

    # Create game objects
    player = Player(100, 100, 50, 50)
    objects = create_challenging_map(WIDTH, HEIGHT, block_size)
    health_bar = HealthBar(block_size*7, 10, 200, 20)

    # Camera scrolling variables
    offset_x = 0  # Current camera offset
    scroll_area_width = 200  # Distance from edge before camera starts scrolling

    # Main game loop
    run = True
    while run:
        clock.tick(FPS)  # Maintain consistent framerate
        if player.health <= 0 :
            waiting = game_over(window,WIDTH, HEIGHT,type="Game Over", score=10)
            if not waiting:
                main(window)
        if player.rect.top > HEIGHT:
            waiting = game_over(window,WIDTH, HEIGHT,type="You Won", score=100)
            if not waiting:
                main(window)

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
        player.loop(FPS,health_bar)  # Update player physics and animation
        for obj in objects:
            if isinstance(obj, Fire):
                obj.loop()  # Update fire animation
        handle_move(player, objects)  # Handle player movement and collisions
        
        # Draw everything
        draw(window, background, bg_image, player, objects,health_bar, offset_x)

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