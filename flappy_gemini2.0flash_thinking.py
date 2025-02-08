import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Colors
light_blue_shades = [(173, 216, 230), (224, 255, 255), (176, 224, 230)] # Light Blue, White Smoke, Light Cyan
dark_colors = [(34, 34, 34), (51, 51, 51), (68, 68, 68), (85, 85, 85), (102, 102, 102)] # Dark Grays
dark_brown = (101, 67, 33)
yellow = (255, 255, 0)
dark_green = (0, 100, 0)
light_brown = (139, 69, 19)
dark_gray_shades = [(105, 105, 105), (119, 136, 153), (128, 128, 128)] # Dim Gray, Light Slate Gray, Gray
black = (0, 0, 0)
white = (255, 255, 255)

# Choose random background color (light shade)
background_color = random.choice(light_blue_shades)

# Bird properties
bird_x = 80
bird_y = screen_height // 2
bird_radius = 15
bird_size = 25
bird_velocity = 0
gravity = 0.5
flap_power = -10
bird_shapes = ["circle", "square", "triangle"]
bird_shape = random.choice(bird_shapes)
bird_color = random.choice(dark_colors)

# Land properties
land_height = 100
land_color = random.choice([dark_brown, yellow])

# Pipe properties
pipe_width = 60
pipe_gap = 150
pipe_velocity = -3
pipe_colors = [dark_green, light_brown, random.choice(dark_gray_shades)]
pipes = []
last_pipe_time = pygame.time.get_ticks()
pipe_spawn_interval = 1500 # milliseconds
score = 0
best_score = 0
font = pygame.font.Font(None, 36)
game_over = False

def reset_game():
    global bird_y, bird_velocity, pipes, score, game_over, last_pipe_time, background_color, bird_shape, bird_color, land_color, pipe_colors
    bird_y = screen_height // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False
    last_pipe_time = pygame.time.get_ticks()
    background_color = random.choice(light_blue_shades)
    bird_shape = random.choice(bird_shapes)
    bird_color = random.choice(dark_colors)
    land_color = random.choice([dark_brown, yellow])
    pipe_colors = [dark_green, light_brown, random.choice(dark_gray_shades)]


def create_pipe():
    pipe_color = random.choice(pipe_colors)
    pipe_height = random.randint(100, screen_height - land_height - pipe_gap - 50) # Ensure pipe gap is within screen
    top_pipe_rect = pygame.Rect(screen_width, 0, pipe_width, pipe_height)
    bottom_pipe_y = pipe_height + pipe_gap
    bottom_pipe_rect = pygame.Rect(screen_width, bottom_pipe_y, pipe_width, screen_height - bottom_pipe_y - land_height)
    return {"top": top_pipe_rect, "bottom": bottom_pipe_rect, "color": pipe_color, "passed": False}

def draw_bird(shape):
    if shape == "circle":
        pygame.draw.circle(screen, bird_color, (bird_x, int(bird_y)), bird_radius)
    elif shape == "square":
        pygame.draw.rect(screen, bird_color, (bird_x - bird_size//2, int(bird_y) - bird_size//2, bird_size, bird_size))
    elif shape == "triangle":
        points = [(bird_x, int(bird_y) - bird_size//2), (bird_x - bird_size//2, int(bird_y) + bird_size//2), (bird_x + bird_size//2, int(bird_y) + bird_size//2)]
        pygame.draw.polygon(screen, bird_color, points)


def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, pipe["color"], pipe["top"])
        pygame.draw.rect(screen, pipe["color"], pipe["bottom"])

def move_pipes():
    global pipes, score
    new_pipes = []
    for pipe in pipes:
        pipe["top"].x += pipe_velocity
        pipe["bottom"].x += pipe_velocity
        if pipe["top"].right > 0:
            new_pipes.append(pipe)
            if not pipe["passed"] and pipe["top"].right < bird_x:
                score += 1
                pipe["passed"] = True
    pipes = new_pipes

def check_collision():
    global game_over, best_score
    bird_rect_circle = pygame.Rect(bird_x - bird_radius, int(bird_y) - bird_radius, bird_radius * 2, bird_radius * 2) # Approximate rect for circle collision
    bird_rect_square = pygame.Rect(bird_x - bird_size//2, int(bird_y) - bird_size//2, bird_size, bird_size)
    bird_rect_triangle = pygame.Rect(bird_x - bird_size//2, int(bird_y) - bird_size//2, bird_size, bird_size)

    bird_rect = bird_rect_circle if bird_shape == "circle" else bird_rect_square if bird_shape == "square" else bird_rect_triangle

    if bird_y > screen_height - land_height or bird_y < 0:
        game_over = True
        best_score = max(score, best_score)
        return

    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            game_over = True
            best_score = max(score, best_score)
            return

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    bird_velocity = flap_power # Accelerate with multiple space presses
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity

        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > pipe_spawn_interval:
            pipes.append(create_pipe())
            last_pipe_time = current_time

        move_pipes()
        check_collision()

    # Drawing
    screen.fill(background_color)

    draw_pipes()

    pygame.draw.rect(screen, land_color, (0, screen_height - land_height, screen_width, land_height)) # Land

    draw_bird(bird_shape)

    # Display score
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

    if game_over:
        best_score_text = font.render(f"Best Score: {best_score}", True, black)
        game_over_text = font.render("Game Over - Press SPACE to Restart, Q or ESC to Quit", True, black)

        screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2 - game_over_text.get_height()//2 - 20 ))
        screen.blit(best_score_text, (screen_width//2 - best_score_text.get_width()//2, screen_height//2 + 20))


    pygame.display.flip()
    pygame.time.delay(16) # Approx 60 FPS

pygame.quit()