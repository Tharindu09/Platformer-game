import pygame

class HealthBar:
    def __init__(self, x, y, width, height,max_health=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = max_health
        self.color = (255, 0, 0)  # Red color for health bar
        self.background_color = (0, 0, 0)  # Black color for background
    
    def update_health(self, health):
        self.health = health
    
    def draw(self, surface):
        # Draw the background rectangle
        pygame.draw.rect(surface, self.background_color, (self.x, self.y, self.width, self.height))
        
        # Calculate the width of the health bar based on health percentage
        health_width = int(self.width * (self.health / 100))
        
        # Draw the health bar rectangle
        pygame.draw.rect(surface, self.color, (self.x, self.y, health_width, self.height))