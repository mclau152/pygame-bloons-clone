import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Shooter with Gravity and Piercing")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player settings
player_radius = 20
player_x = WIDTH // 2
player_y = HEIGHT // 2
arrow_length = 40
arrow_angle = 0
power = 50
max_power = 100

# Projectile settings
projectile_radius = 5
projectiles = []

# Physics settings
gravity = 0.5

# Game settings
max_shots = 10
shots_left = max_shots
level = 1
base_targets = 5

def create_targets(num):
    return [pygame.Rect(random.randint(0, WIDTH -150- target_size), random.randint(0, HEIGHT -150- target_size), target_size, target_size) for _ in range(num)]

def reset_level():
    global targets, shots_left
    shots_left = max_shots
    num_targets = base_targets + level - 1
    targets = create_targets(num_targets)

def next_level():
    global level
    level += 1
    reset_level()

# Target settings
target_size = 30
reset_level()

# Game loop
clock = pygame.time.Clock()

game_over = False
won = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and shots_left > 0:
                speed = power / 5
                projectiles.append([player_x, player_y, arrow_angle, speed, 0])
                shots_left -= 1
            elif event.key == pygame.K_r and game_over and not won:
                game_over = False
                won = False
                projectiles.clear()
                reset_level()
            elif event.key == pygame.K_n and game_over and won:
                game_over = False
                won = False
                projectiles.clear()
                next_level()

    if not game_over:
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            arrow_angle += 3
        if keys[pygame.K_RIGHT]:
            arrow_angle -= 3
        if keys[pygame.K_UP]:
            power = min(power + 2, max_power)
        if keys[pygame.K_DOWN]:
            power = max(power - 2, 0)

        # Update projectiles
        for proj in projectiles:
            proj[0] += math.cos(math.radians(proj[2])) * proj[3]
            proj[1] -= math.sin(math.radians(proj[2])) * proj[3] - proj[4]
            proj[4] += gravity

        # Check for collisions
        for proj in projectiles[:]:
            for target in targets[:]:
                if target.collidepoint(proj[0], proj[1]):
                    targets.remove(target)
            
            # Remove projectile only if it's out of bounds
            if proj[0] < 0 or proj[0] > WIDTH or proj[1] > HEIGHT:
                projectiles.remove(proj)

    # Clear the screen
    screen.fill(WHITE)

    # Draw targets
    for target in targets:
        pygame.draw.rect(screen, BLUE, target)

    # Draw player
    pygame.draw.circle(screen, RED, (int(player_x), int(player_y)), player_radius)

    # Draw arrow
    end_x = player_x + arrow_length * math.cos(math.radians(arrow_angle))
    end_y = player_y - arrow_length * math.sin(math.radians(arrow_angle))
    pygame.draw.line(screen, BLACK, (player_x, player_y), (end_x, end_y), 2)

    # Draw power bar
    font = pygame.font.Font(None, 36)
    power_text = font.render("Power", True, BLACK)
    screen.blit(power_text, (WIDTH - power_text.get_width() - 600, 5))
    power_bar_width = 100
    power_bar_height = 10
    power_bar_x = 10
    power_bar_y = 10
    pygame.draw.rect(screen, BLACK, (power_bar_x, power_bar_y, power_bar_width, power_bar_height), 1)
    pygame.draw.rect(screen, GREEN, (power_bar_x, power_bar_y, power * power_bar_width // max_power, power_bar_height))

    # Draw projectiles
    for proj in projectiles:
        pygame.draw.circle(screen, BLACK, (int(proj[0]), int(proj[1])), projectile_radius)

    # Draw shots left and level
    font = pygame.font.Font(None, 36)
    shots_text = font.render(f"Shots left: {shots_left}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(shots_text, (WIDTH - shots_text.get_width() - 10, 10))
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 50))

    # Check for win/lose condition
    if not targets:
        game_over = True
        won = True
        message = "You Win! Press N for next level"
    elif shots_left == 0 and not projectiles:
        game_over = True
        won = False
        message = "You Lose! Press R to retry"

    if game_over:
        game_over_text = font.render(message, True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
