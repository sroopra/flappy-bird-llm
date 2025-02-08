import pygame
import random
import time

pygame.init()

# Screen dimensions
width = 288
height = 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Colors
light_blue = (135, 206, 235)
dark_brown = (101, 67, 33)
yellow = (255, 255, 0)
dark_green = (0, 100, 0)
light_brown = (210, 180, 140)
dark_gray = (105, 105, 105)

def random_light_color():
    r = random.randint(150, 255)
    g = random.randint(150, 255)
    b = random.randint(150, 255)
    return (r, g, b)

def random_dark_color():
    r = random.randint(0, 100)
    g = random.randint(0, 100)
    b = random.randint(0, 100)
    return (r, g, b)

# Bird
bird_x = 50
bird_y = height // 2
bird_radius = 15
bird_shape = random.choice(["circle", "square", "triangle"])
bird_color = random_dark_color()
gravity = 0.5
bird_velocity = 0
flap_power = -10

# Pipes
pipe_width = 50
pipe_gap = 150
pipe_x_positions = []
pipe_heights = []

def generate_pipe():
    height = random.randint(100, height - pipe_gap - 100)
    pipe_heights.append(height)
    pipe_heights.append(height + pipe_gap)  # Bottom pipe
    pipe_x_positions.append(width)
    pipe_x_positions.append(width)


# Land
land_height = 50
land_color = random.choice([dark_brown, yellow])

# Score
score = 0
font = pygame.font.Font(None, 36)
best_score = 0

# Game state
game_over = False

# Initial pipes
generate_pipe()
generate_pipe()

# Game loop
running = True
background_color = light_blue #random_light_color()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                bird_y = height // 2
                bird_velocity = 0
                score = 0
                pipe_x_positions = []
                pipe_heights = []
                generate_pipe()
                generate_pipe()
            elif event.key == pygame.K_SPACE and not game_over:
                bird_velocity = flap_power
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False


    if not game_over:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe movement
        for i in range(len(pipe_x_positions)):
            pipe_x_positions[i] -= 5

            # Check for score
            if pipe_x_positions[i] < bird_x and i % 2 == 0 and pipe_x_positions[i] + pipe_width >= bird_x :
                score += 1

            if pipe_x_positions[i] < -pipe_width:
                pipe_x_positions.pop(i)
                pipe_heights.pop(i)
                if i % 2 == 0: #only generate when top pipe is removed
                    generate_pipe()
                break

        # Collision detection
        if bird_y > height - land_height or bird_y < 0:
            game_over = True
        for i in range(0, len(pipe_x_positions), 2):
            if bird_x + bird_radius > pipe_x_positions[i] and bird_x - bird_radius < pipe_x_positions[i] + pipe_width:
                if bird_y - bird_radius < pipe_heights[i] or bird_y + bird_radius > pipe_heights[i] + pipe_gap:
                    game_over = True
                    break

    # Drawing
    screen.fill(background_color)

    # Pipes
    pipe_color = random.choice([dark_green, light_brown, dark_gray])
    for i in range(len(pipe_x_positions)):
        pygame.draw.rect(screen, pipe_color, (pipe_x_positions[i], 0 if i % 2 == 0 else pipe_heights[i] + pipe_gap, pipe_width, pipe_heights[i] if i % 2 == 0 else height - land_height - (pipe_heights[i] + pipe_gap)))

    # Land
    pygame.draw.rect(screen, land_color, (0, height - land_height, width, land_height))

    # Bird
    if bird_shape == "circle":
        pygame.draw.circle(screen, bird_color, (bird_x, bird_y), bird_radius)
    elif bird_shape == "square":
        pygame.draw.rect(screen, bird_color, (bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2))
    elif bird_shape == "triangle":
        pygame.draw.polygon(screen, bird_color, [(bird_x, bird_y - bird_radius), (bird_x + bird_radius, bird_y + bird_radius), (bird_x - bird_radius, bird_y + bird_radius)])

    # Score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (width - score_text.get_width() - 10, 10))

    if game_over:
        best_score = max(best_score, score)
        game_over_text = font.render("Game Over!", True, (0, 0, 0))
        best_score_text = font.render(f"Best: {best_score}", True, (0, 0, 0))
        restart_text = font.render("Press SPACE to restart", True, (0, 0, 0))

        text_x = width // 2
        text_y = height // 2

        screen.blit(game_over_text, (text_x - game_over_text.get_width() // 2, text_y - 50))
        screen.blit(best_score_text, (text_x - best_score_text.get_width() // 2, text_y))
        screen.blit(restart_text, (text_x - restart_text.get_width() // 2, text_y + 50))

    pygame.display.flip()
    time.sleep(1/60)

pygame.quit()