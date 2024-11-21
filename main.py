import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen dimensions and display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rotating Sprite')

# Load the sprite image
sprite = pygame.image.load('player.png')  # Replace with your image path
# Scale the sprite to 128x128 px
sprite = pygame.transform.smoothscale(sprite.convert_alpha(), (128, 128))
sprite_rect = sprite.get_rect()
sprite_center = (screen_width // 2, screen_height // 2)  # Center of the screen
sprite_rect.center = sprite_center

# Clock to control the frame rate
clock = pygame.time.Clock()

# Rotation variables
angle = 0  # Initial rotation angle
rotation_speed = 1  # Speed of rotation (positive for clockwise, negative for counterclockwise)
rotation_direction = -1  # 1 for clockwise, -1 for counterclockwise

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game loop
while True:
    # Handle events (e.g., quitting the app)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    # Draw the rotated sprite
    screen.blit(rotated_sprite, rotated_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)  # 60 FPS