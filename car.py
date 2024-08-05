import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Racing Game")

# Load background image
background = pygame.image.load("background.jpg")
rect_bg = background.get_rect()
rect_bg.y = -900

# Load player car image
player_car_image = pygame.image.load("car.png")
player_car_width = 60
player_car_height = 120

player_car_rect = player_car_image.get_rect()
player_car_rect.x = screen_width // 2 - player_car_width // 2
player_car_rect.bottom = screen_height - 10
player_car_speed = 5

# Load AI car image
ai_car_image = pygame.image.load("ai_car.png")
ai_car_width = 60
ai_car_height = 120

ai_car_rect = ai_car_image.get_rect()
ai_car_rect.x = random.randint(0, screen_width - ai_car_width)
ai_car_rect.bottom = screen_height + ai_car_height
ai_car_speed = 3

# Load obstacle image
obstacle_image = pygame.image.load("obstacle.png")
obstacle_width = 50
obstacle_height = 50
obstacle_rect = obstacle_image.get_rect()
obstacle_rect.x = random.randint(0, screen_width - obstacle_width)
obstacle_rect.y = -obstacle_height
obstacle_speed = 4

# Load font for text
font = pygame.font.Font(None, 36)

# Game variables
score = 0
last_score_time = pygame.time.get_ticks()
penalty = 10

# Game loop
running = True
clock = pygame.time.Clock()

game_over = False
name='arik'

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_car_rect.x > 0:
            player_car_rect.x -= player_car_speed
        if keys[pygame.K_RIGHT] and player_car_rect.x < screen_width - player_car_width:
            player_car_rect.x += player_car_speed
        if keys[pygame.K_UP] and player_car_rect.y > 0:
            player_car_rect.y -= player_car_speed
        if keys[pygame.K_DOWN] and player_car_rect.y < screen_height - player_car_height:
            player_car_rect.y += player_car_speed

        # AI car movement
        if ai_car_rect.y < -ai_car_height:
            ai_car_rect.x = random.randint(0, screen_width - ai_car_width)
            ai_car_rect.y = screen_height + ai_car_height
            ai_car_speed = random.randint(2, 5)
        else:
            ai_car_rect.y -= ai_car_speed

        # Update obstacle position
        obstacle_rect.y += obstacle_speed
        if obstacle_rect.top > screen_height:
            obstacle_rect.x = random.randint(0, screen_width - obstacle_width)
            obstacle_rect.y = -obstacle_height

        # Collision detection with AI car
        if player_car_rect.colliderect(ai_car_rect):
            ai_car_rect.y = -100
            score -= penalty


        # score every 30 seconds
        current_time = pygame.time.get_ticks()
        if current_time - last_score_time >= 1000:
            score += 1
            last_score_time = current_time

        # Collision detection with obstacle
        if player_car_rect.colliderect(obstacle_rect):
            score -= 1
            obstacle_rect.top = screen_height

    # Draw the screen
    rect_bg.y += 4
    if rect_bg.y >= -4:
        rect_bg.y = -799
    screen.blit(background, rect_bg)
    screen.blit(player_car_image, player_car_rect)
    screen.blit(ai_car_image, ai_car_rect)
    screen.blit(obstacle_image, obstacle_rect)

    # Render score text
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if game_over:
        text = font.render("You Lose", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

    pygame.display.update()

    clock.tick(60)

# Game over
pygame.quit()
