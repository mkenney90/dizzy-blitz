import pygame
import sys
import math

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, color, bullets, player, increase_score):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 1
        self.player = player
        self.bullets = bullets # for collision reference
        self.increase_score = increase_score
        pygame.draw.ellipse(self.image, color, self.image.get_rect())  # Red ellipse

    def update(self, bullets):
        # Movement
        dx = self.player[0] - self.rect.centerx
        dy = self.player[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))

        # Calculate the distance (length of the vector)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Normalize the vector (optional, to get direction only)
        dx_normalized = dx / (distance or 1)
        dy_normalized = dy / (distance or 1)

        self.rect.x += dx_normalized * self.speed
        self.rect.y += dy_normalized * self.speed
        self.bullets = bullets

        # Destroy if it goes off-screen
        # if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height:
        #     self.kill()

        # Collision with bullets
        _b = pygame.sprite.spritecollideany(self, self.bullets)
        if _b:
            print("COLLISION")
            self.kill()
            _b.kill()
            self.increase_score(1)