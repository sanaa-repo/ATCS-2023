import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1060, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kung Fu Fighter")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load background
background = pygame.image.load("MazeKungFu/assets/images/dojo_bknd.png")  # Replace with your background image
background = pygame.transform.scale(background, (width,height))
# Load kung fu fighter
fighter_image = pygame.image.load("MazeKungFu/assets/images/kung_fu_fighter_standing.png")  # Replace with your fighter image
fighter_height, fighter_width = 200, 200
fighter_image = pygame.transform.scale(fighter_image, (fighter_height,fighter_width))
fighter_x, fighter_y = 0, 600
fighter_speed = 5

# Set initial direction
direction = 1  # 1 for right, -1 for left

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the fighter back and forth

    keys = pygame.key.get_pressed()

    # Move the fighter based on arrow key input
    if keys[pygame.K_LEFT] and fighter_x > 0:
        fighter_image = pygame.image.load("MazeKungFu/assets/images/kung_fu_fighter_standing.png")  # Replace with your fighter image
        fighter_height, fighter_width = 200, 200
        fighter_image = pygame.transform.scale(fighter_image, (fighter_height,fighter_width))

        fighter_x -= fighter_speed
    if keys[pygame.K_RIGHT] and fighter_x < width - fighter_width:
        fighter_image = pygame.image.load("MazeKungFu/assets/images/kung_fu_fighter_standing.png")  # Replace with your fighter image
        fighter_height, fighter_width = 200, 200
        fighter_image = pygame.transform.scale(fighter_image, (fighter_height,fighter_width))

        fighter_x += fighter_speed
    if keys[pygame.K_UP] and fighter_x < width - fighter_width:
        fighter_image = pygame.image.load("MazeKungFu/assets/images/kung_fu_fighter_punch.png")  # Replace with your fighter image
        fighter_height, fighter_width = 200, 200
        fighter_image = pygame.transform.scale(fighter_image, (fighter_height,fighter_width))
    if keys[pygame.K_DOWN] and fighter_x < width - fighter_width:
        fighter_image = pygame.image.load("MazeKungFu/assets/images/kung_fu_fighter_kick.png")  # Replace with your fighter image
        fighter_height, fighter_width = 200, 200
        fighter_image = pygame.transform.scale(fighter_image, (fighter_height,fighter_width))





    # Check boundaries to change direction
    if fighter_x <= 0 or fighter_x >= width - fighter_width:
        direction *= -1  # Change direction when hitting the screen edges

    # Clear the screen
    screen.fill(white)

    # Draw background
    screen.blit(background, (0, 0))

    # Draw kung fu fighter
    screen.blit(fighter_image, (fighter_x, fighter_y))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
