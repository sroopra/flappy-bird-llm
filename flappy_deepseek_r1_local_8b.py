import pygame
import random
random.seed(42)  # For reproducibility, though in real code remove this

# Initialize Pygame and display
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Colors definitions
background_colors = ['#87CEEB', '#9BCD7F', '#E0FFFF']  # Light blue, light brown/yellow, etc.
bird_colors = ['#333333', '#666666', '#999999']  # Dark colors for bird
pipe_colors = ['#006B3C', '#8B4513', '#4A2B4C']  # Dark green, dark brown, dark gray

# Bird shapes definitions
def create_bird(shape):
    if shape == 'square':
        return pygame.Rect(400 - 50, 300 - 50), bird_colors[random.randint(0, 2)]
    elif shape == 'circle':
        return pygame.draw.circle((400, 300), *bird_colors[random.randint(0, 2)])
    else:  # triangle
        vertices = [(400 - 30, 300 - 20), (400 + 30, 300 - 20), (400, 300 + 40)]
        return pygame.draw_polygon(vertices, bird_colors[random.randint(0, 2)])

# Function to generate pipes
def create_pipe():
    x_pos = random.randint(0, width)
    y_pos = random.randint(50, height - 100)
    pipe_width = 60
    gap_height = 150
    return {
        'x': x_pos,
        'y': y_pos,
        'width': pipe_width,
        'height': gap_height,
        'color': pipe_colors[random.randint(0, 2)]
    }

# Initialize game variables
bird = None
score = 0
best_score = 0
pipes = []
running = True
current_shape = 'square'

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if bird is not None:
                bird['y'] -= 10

    # Bird movement
    if bird is not None:
        bird['y'] += 10

    # Check for collisions
    collision = False
    for p in pipes:
        if (bird['x'] - p['width']/2 >= p['x']) and \
           (bird['x'] + p['width']/2 <= p['x'] + p['width']):
            if bird['y'] < p['y'] or bird['y'] > p['y'] + p['height']:
                collision = True
    # Check ground collision
    if bird is not None and bird['y'] >= height - 50:
        collision = True

    # Update game state
    if collision:
        running = False
        print(f"Game Over! Score: {score}")
        if score > best_score:
            best_score = score
        pygame.quit()
        exit()

    # Generate new pipes
    if len(pipes) < 5 and random.random() < 0.02:
        pipes.append(create_pipe())

    # Update pipes positions
    for i, p in enumerate(pipes):
        p['x'] += 2

    # Check for scoring
    if bird is not None:
        for p in pipes:
            if p['y'] <= bird['y'] < p['y'] + p['height']:
                score += 1
                break

    # Clear screen and redraw elements
    screen.fill(background_colors[random.randint(0, len(background_colors))])
    for p in pipes:
        pygame.draw.rect(screen, p['color'], (p['x'], p['y'], p['width'], p['height']))
    if bird is not None:
        current_shape = create_bird(current_shape)
        screen.blit(current_shape[0], current_shape[1])

    # Display score
    font = pygame.font.Font(None, 74)
    text = font.render(f"{score}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(width//2, 50))
    screen.blit(text, text_rect)

    # Display best score if game over
    if not running:
        font = pygame.font.Font(None, 74)
        text = font.render(f"Best: {best_score}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width//2, height//2 + 100))
        screen.blit(text, text_rect)

    pygame.display.flip()
