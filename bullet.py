import pygame
import sys
import math

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, color):
        super().__init__()
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA)  # Bullet size
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 5  # Bullet speed
        pygame.draw.ellipse(self.image, color, self.image.get_rect())  # Yellow ellipse

    def update(self, screen_width, screen_height):
        # Move the bullet in the direction of the angle
        radians = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(radians)
        self.rect.y -= self.speed * math.sin(radians)

        # Remove bullet if it goes off-screen
        if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height:
            self.kill()