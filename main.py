import random
import pygame
import sys
import math
from bullet import Bullet
from enemy import Enemy

# Initialize Pygame
pygame.init()

COLOR_ENEMY = (204, 75, 24)
COLOR_SECONDARY = (225, 151, 36)

# Set up screen dimensions and display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dizzy Blitz')

# Load the sprite image
sprite = pygame.image.load('player.png')  # Replace with your image path
# Scale the sprite to 128x128 px
sprite = pygame.transform.smoothscale(sprite.convert_alpha(), (128, 128))

sprite = pygame.transform.rotate(sprite, -90)
sprite_rect = sprite.get_rect()
sprite_center = (screen_width // 2, screen_height // 2)  # Center of the screen
sprite_rect.center = sprite_center

# UI
top_bar_height = 35
top_bar = pygame.Surface((screen_width, top_bar_height), pygame.SRCALPHA)
ui_font = pygame.font.Font('fonts/BAHNSCHRIFT.ttf', 20)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Rotation variables
angle = 0  # Initial rotation angle

offset_marker = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
offset_marker.fill((0,0,0,0))
offset_rect = offset_marker.get_rect(center=(sprite_center))
pygame.draw.circle(offset_marker, (255, 255, 0), sprite_center, 5)

rotation_speed = 2  # Speed of rotation (positive for clockwise, negative for counterclockwise)
rotation_direction = -1  # 1 for clockwise, -1 for counterclockwise

# Create a sprite group to hold all bullets
bullets = pygame.sprite.Group()

# Enemy group
enemies = pygame.sprite.Group()

# Score
score = 0

def increase_score(points):
    global score
    score = score + points

# Timing for shooting delay
last_shot_time = 0
shoot_delay = 400  # Delay in milliseconds

# Timing for enemy spawn
last_enemy_time = 0
enemy_delay = 2000

# Game loop
while True:
    # Handle events (e.g., quitting the app)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle spacebar press for firing bullets
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if keys[pygame.K_SPACE]:
        # Only shoot if the delay has passed
        if current_time - last_shot_time >= shoot_delay:
            # Calculate the position of the barrel based on the sprite's rotation
            barrel_length = 44  # Distance from the center of the sprite to the barrel tip
            bullet_x = sprite_rect.centerx + barrel_length * math.cos(math.radians(angle - rotation_speed * 5))
            bullet_y = sprite_rect.centery - barrel_length * math.sin(math.radians(angle - rotation_speed * 5))

            # Create a bullet at the calculated position and fire it in the direction of the sprite's angle
            bullet = Bullet(bullet_x, bullet_y, angle, COLOR_SECONDARY)
            bullets.add(bullet)
            last_shot_time = current_time  # Update the last shot time

    # spawning enemies
    _r = random.randint(0,3)
    if _r == 0:
        spawn_x = -20
        spawn_y = random.randint(0,screen_height)
    elif _r == 1:
        spawn_x = screen_width + 20
        spawn_y = random.randint(0,screen_height)
    elif _r == 2:
        spawn_x = random.randint(0,screen_width)
        spawn_y = -20
    else:
        spawn_x = random.randint(0,screen_width)
        spawn_y = screen_height + 20

    if current_time - last_enemy_time >= enemy_delay:
        enemy = Enemy(spawn_x, spawn_y, 0, COLOR_ENEMY, bullets, sprite_center, increase_score)
        enemies.add(enemy)
        last_enemy_time = current_time
    
    
    # Update the rotation angle based on the speed and direction
    angle += rotation_speed * rotation_direction

    # Ensure the angle stays within 0-360 degrees
    if angle >= 360:
        angle -= 360
    elif angle < 0:
        angle += 360

    # Rotate the sprite image
    rotated_sprite = pygame.transform.rotate(sprite, angle)

    # Get the new rect of the rotated sprite
    rotated_rect = rotated_sprite.get_rect()

    # Keep the center of the rotated sprite at the center of the screen
    rotated_rect.center = sprite_center

    # Fill the screen with a background color (black in this case)
    screen.fill((0, 0, 0))

    # Draw all bullets
    bullets.update(screen_width, screen_height)
    bullets.draw(screen)

    # Draw enemies
    enemies.update(bullets)
    enemies.draw(screen)

    # Draw the rotated sprite
    screen.blit(rotated_sprite, rotated_rect.topleft)

    # draw and update UI
    text = ui_font.render('SCORE ' + str(score), True, (10,10,10))
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    pygame.draw.rect(top_bar, (200, 200, 200), (0, 0, screen_width, top_bar_height))
    top_bar.blit(text, text_rect)
    screen.blit(top_bar, (0, 0))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)  # 60 FPS
