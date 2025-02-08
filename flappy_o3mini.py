import pygame
import random
import sys

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game constants
GRAVITY = 0.5
JUMP_BOOST = -8  # each SPACE press adds this (more negative means upward)
LAND_HEIGHT = 50
PIPE_WIDTH = 50
PIPE_GAP = 150  # vertical gap between top and bottom pipes
PIPE_SPEED = 3   # how fast pipes move leftwards

# Color choices
# Light shades for background (start with light blue)
LIGHT_COLORS = [
    (173, 216, 230),  # light blue
    (255, 239, 213),  # papaya whip
    (255, 228, 225),  # misty rose
    (240, 248, 255),  # alice blue
    (245, 245, 220)   # beige
]

# Dark colors for the bird
DARK_COLORS = [
    (0, 0, 0),        # black
    (139, 0, 0),      # dark red
    (0, 100, 0),      # dark green
    (25, 25, 112),    # midnight blue
    (75, 0, 130)      # indigo
]

# Land colors (choose between dark brown and yellow)
LAND_COLORS = [
    (101, 67, 33),    # dark brown
    (255, 215, 0)     # yellow (golden)
]

# Pipe colors (choose between dark green, light brown, and dark gray)
PIPE_COLORS = [
    (0, 128, 0),      # dark green
    (181, 101, 29),   # light brown
    (64, 64, 64)      # dark gray
]

# Bird shapes: square, circle or triangle
BIRD_SHAPES = ["square", "circle", "triangle"]
BIRD_X = 50
BIRD_SIZE = 20  # size of the bird’s bounding box

# Font definitions
score_font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

# Global game state variables
first_run = True  # to start with light blue background
score = 0
best_score = 0
game_over = False

# These globals will be reset at game start/restart:
bird_y = HEIGHT // 2
bird_vel = 0
bird_shape = random.choice(BIRD_SHAPES)
bird_color = random.choice(DARK_COLORS)
background_color = (173, 216, 230)  # light blue initially
land_color = random.choice(LAND_COLORS)
pipes = []  # each pipe will be a dict: { 'x': ..., 'gap_y': ..., 'passed': bool, 'color': ... }
last_pipe_time = pygame.time.get_ticks()
next_pipe_interval = random.randint(1500, 2500)  # in milliseconds

def reset_game():
    """Reset all game state variables for a new run."""
    global bird_y, bird_vel, pipes, score, bird_shape, bird_color
    global background_color, land_color, last_pipe_time, next_pipe_interval, first_run, game_over

    bird_y = HEIGHT // 2
    bird_vel = 0
    pipes = []
    score = 0
    bird_shape = random.choice(BIRD_SHAPES)
    bird_color = random.choice(DARK_COLORS)
    if first_run:
        background_color = (173, 216, 230)  # light blue on first run
        first_run = False
    else:
        background_color = random.choice(LIGHT_COLORS)
    land_color = random.choice(LAND_COLORS)
    last_pipe_time = pygame.time.get_ticks()
    next_pipe_interval = random.randint(1500, 2500)
    game_over = False

# Start the first game
reset_game()

# Main game loop
running = True
while running:
    clock.tick(60)  # 60 frames per second
    current_time = pygame.time.get_ticks()

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Quit the game if Esc or q is pressed
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
                pygame.quit()
                sys.exit()
            # SPACE press: either restart or give the bird an upward boost
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    # Each SPACE press adds an upward boost to the bird (cumulative acceleration)
                    bird_vel += JUMP_BOOST

    if not game_over:
        # --- Update Bird ---
        bird_vel += GRAVITY
        bird_y += bird_vel

        # --- Create New Pipes at Random Intervals ---
        if current_time - last_pipe_time > next_pipe_interval:
            # Choose a random vertical position for the gap.
            # Ensure the gap is not too high or too low.
            gap_y = random.randint(100, HEIGHT - LAND_HEIGHT - PIPE_GAP - 100)
            pipes.append({
                'x': WIDTH,
                'gap_y': gap_y,
                'passed': False,
                'color': random.choice(PIPE_COLORS)
            })
            last_pipe_time = current_time
            next_pipe_interval = random.randint(1500, 2500)

        # --- Move Pipes ---
        for pipe in pipes:
            pipe['x'] -= PIPE_SPEED

        # Remove pipes that have moved off the screen
        pipes = [pipe for pipe in pipes if pipe['x'] + PIPE_WIDTH > 0]

        # --- Collision Detection ---
        # Create a rectangle for the bird
        bird_rect = pygame.Rect(BIRD_X, int(bird_y), BIRD_SIZE, BIRD_SIZE)
        # Check collision with land (or going above the screen)
        if bird_y + BIRD_SIZE > HEIGHT - LAND_HEIGHT or bird_y < 0:
            game_over = True
            if score > best_score:
                best_score = score

        # Check collision with each pipe (both top and bottom parts)
        for pipe in pipes:
            top_pipe_rect = pygame.Rect(pipe['x'], 0, PIPE_WIDTH, pipe['gap_y'])
            bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['gap_y'] + PIPE_GAP, PIPE_WIDTH,
                                           (HEIGHT - LAND_HEIGHT) - (pipe['gap_y'] + PIPE_GAP))
            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                game_over = True
                if score > best_score:
                    best_score = score
                break

        # --- Update Score ---
        # Increase the score if the bird has passed a pipe
        for pipe in pipes:
            if not pipe['passed'] and pipe['x'] + PIPE_WIDTH < BIRD_X:
                pipe['passed'] = True
                score += 1

    # --- Drawing ---
    screen.fill(background_color)

    # Draw pipes
    for pipe in pipes:
        # Top pipe
        top_rect = pygame.Rect(pipe['x'], 0, PIPE_WIDTH, pipe['gap_y'])
        pygame.draw.rect(screen, pipe['color'], top_rect)
        # Bottom pipe
        bottom_rect = pygame.Rect(pipe['x'], pipe['gap_y'] + PIPE_GAP, PIPE_WIDTH,
                                   (HEIGHT - LAND_HEIGHT) - (pipe['gap_y'] + PIPE_GAP))
        pygame.draw.rect(screen, pipe['color'], bottom_rect)

    # Draw the land at the bottom
    land_rect = pygame.Rect(0, HEIGHT - LAND_HEIGHT, WIDTH, LAND_HEIGHT)
    pygame.draw.rect(screen, land_color, land_rect)

    # Draw the bird in its chosen shape and color.
    # Use the same bounding rectangle for collision and drawing.
    bird_rect = pygame.Rect(BIRD_X, int(bird_y), BIRD_SIZE, BIRD_SIZE)
    if bird_shape == "square":
        pygame.draw.rect(screen, bird_color, bird_rect)
    elif bird_shape == "circle":
        center = (BIRD_X + BIRD_SIZE // 2, int(bird_y) + BIRD_SIZE // 2)
        radius = BIRD_SIZE // 2
        pygame.draw.circle(screen, bird_color, center, radius)
    elif bird_shape == "triangle":
        # Draw an isosceles triangle
        point1 = (BIRD_X, int(bird_y) + BIRD_SIZE)
        point2 = (BIRD_X + BIRD_SIZE // 2, int(bird_y))
        point3 = (BIRD_X + BIRD_SIZE, int(bird_y) + BIRD_SIZE)
        pygame.draw.polygon(screen, bird_color, [point1, point2, point3])

    # Draw the current score at the top right
    score_surface = score_font.render("Score: " + str(score), True, (0, 0, 0))
    score_rect = score_surface.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(score_surface, score_rect)

    # If the game is over, display Game Over and best score text
    if game_over:
        game_over_surface = score_font.render("Game Over!", True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(game_over_surface, game_over_rect)

        best_score_surface = small_font.render("Best Score: " + str(best_score), True, (0, 0, 0))
        best_score_rect = best_score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(best_score_surface, best_score_rect)

        restart_surface = small_font.render("Press SPACE to restart", True, (0, 0, 0))
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(restart_surface, restart_rect)

    pygame.display.flip()
