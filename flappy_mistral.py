import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
LIGHT_BLUE = (135, 206, 250)
DARK_COLORS = [(0, 0, 139), (0, 100, 0), (139, 0, 0)]  # Dark Blue, Dark Green, Dark Red
LIGHT_COLORS = [(173, 216, 230), (240, 230, 140), (210, 180, 140)]  # Light Blue, Light Yellow, Light Brown
DARK_BROWN = (85, 65, 0)
YELLOW = (255, 255, 0)
PIPE_COLORS = [(0, 100, 0), (139, 69, 19), (105, 105, 105)]  # Dark Green, Light Brown, Dark Gray

# Bird shapes
BIRD_SHAPES = ['square', 'circle', 'triangle']

# Game variables
bird_shape = random.choice(BIRD_SHAPES)
bird_color = random.choice(DARK_COLORS)
background_color = random.choice(LIGHT_COLORS)
land_color = random.choice([DARK_BROWN, YELLOW])
pipe_color = random.choice(PIPE_COLORS)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Bird properties
bird_size = 20
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe properties
pipe_width = 70
pipe_height = random.randint(150, 450)
pipe_gap = 150
pipe_x = SCREEN_WIDTH
pipe_velocity = -3

# Score
score = 0
best_score = 0
font = pygame.font.SysFont(None, 36)

def draw_bird():
    if bird_shape == 'square':
        pygame.draw.rect(screen, bird_color, (bird_x, bird_y, bird_size, bird_size))
    elif bird_shape == 'circle':
        pygame.draw.circle(screen, bird_color, (bird_x + bird_size // 2, bird_y + bird_size // 2), bird_size // 2)
    elif bird_shape == 'triangle':
        pygame.draw.polygon(screen, bird_color, [
            (bird_x + bird_size // 2, bird_y),
            (bird_x, bird_y + bird_size),
            (bird_x + bird_size, bird_y + bird_size)
        ])

def draw_pipe():
    pygame.draw.rect(screen, pipe_color, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(screen, pipe_color, (pipe_x, pipe_height + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_height - pipe_gap))

def draw_land():
    pygame.draw.rect(screen, land_color, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

def show_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - 120, 10))

def show_best_score():
    best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
    screen.blit(best_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    restart_text = font.render("Press SPACE to restart or Q to quit", True, (255, 255, 255))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))

def check_collision():
    if bird_y < 0 or bird_y + bird_size > SCREEN_HEIGHT - 50:
        return True
    if bird_x + bird_size > pipe_x and bird_x < pipe_x + pipe_width:
        if bird_y < pipe_height or bird_y + bird_size > pipe_height + pipe_gap:
            return True
    return False

# Game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    bird_y = SCREEN_HEIGHT // 2
                    pipe_x = SCREEN_WIDTH
                    score = 0
                    game_over = False
                else:
                    bird_velocity = jump_strength
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity

        pipe_x += pipe_velocity
        if pipe_x < -pipe_width:
            pipe_x = SCREEN_WIDTH
            pipe_height = random.randint(150, 450)
            score += 1
            best_score = max(best_score, score)

        if check_collision():
            game_over = True

    screen.fill(background_color)
    draw_bird()
    draw_pipe()
    draw_land()
    show_score()
    if game_over:
        show_best_score()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
