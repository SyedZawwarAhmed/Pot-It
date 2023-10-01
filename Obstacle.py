
import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        # Create a surface for the obstacle
        self.image = pygame.Rect(x, y, width, height)
        # self.image.fill(color)

        # Get the Rect object for the obstacle and set its position
        self.rect = self.image
        self.rect.x = x
        self.rect.y = y
