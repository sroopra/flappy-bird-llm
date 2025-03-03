import pygame
import random
from math import sqrt

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 400
HEIGHT = 600
FPS = 30

# Colors helper functions
def random_light_color():
    return (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))

def random_dark_color():
    return (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))

# Randomly choose background color (start with light blue)
BG_COLOR = random_light_color()

# Randomly choose ground color
GROUND_COLOR = random.choice([(139, 68, 19), (255, 215, 0)])

# Randomly choose pipe colors
PIPE_COLORS = [(random_dark_color(), random_dark_color()), 
              (random_dark_color(), random_dark_color()),
              (random_dark_color(), random_dark_color())]

class Bird:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Choose random shape and color for the bird
        self.shape = random.choice(['circle', 'square', 'triangle'])
        self.color = random_dark_color()
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.velocity = 0
        self.acceleration = -1
        
    def jump(self):
        if self.velocity >= -8:
            self.velocity += self.acceleration
            
    def move(self):
        distance = self.velocity * (FPS / 1000)
        self.y -= distance
        self.velocity += 0.5
        
    def draw_circle(self, screen):
        radius = 20
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius)

    def draw_square(self, screen):
        size = 40
        half_size = size // 2
        rect = pygame.Rect(self.x - half_size, self.y - half_size, size, size)
        pygame.draw.rect(screen, self.color, rect)

    def draw_triangle(self, screen):
        points = [(self.x, self.y - 30), (self.x + 15, self.y + 15), 
                  (self.x - 15, self.y + 15)]
        pygame.draw.polygon(screen, self.color, points)

    def draw(self, screen):
        if self.shape == 'circle':
            self.draw_circle(screen)
        elif self.shape == 'square':
            self.draw_square(screen)
        else:
            self.draw_triangle(screen)

class Pipe:
    def __init__(self):
        # Choose random color for the pipe
        self.color = random.choice(PIPE_COLORS)
        self.width = 60
        self.gap = 150
        self.x = WIDTH + random.randint(200, 300)
        self.height = random.randint(80, 120)
        
    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, self.color[0], 
                        (self.x, 0, self.width, HEIGHT - self.gap - self.height))
        # Bottom pipe
        pygame.draw.rect(screen, self.color[1], 
                        (self.x, HEIGHT - self.gap + self.height, self.width, HEIGHT))

def game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    
    bird = Bird()
    pipes = [Pipe()]
    ground_y = HEIGHT - 50
    score = 0
    best_score = 0
    running = True
    
    clock = pygame.time.Clock()
    while running:
        screen.fill(BG_COLOR)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, best_score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
        
        # Ground
        pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, WIDTH, HEIGHT - ground_y))
        
        # Bird movement
        bird.move()
        bird.draw(screen)
        
        # Pipes handling
        new_pipes = []
        for pipe in pipes:
            if pipe.x + pipe.width < 0:
                score += 1
                new_x = pipe.x + random.randint(200, 300)
                new_pipe = Pipe()
                new_pipes.append(new_pipe)
            else:
                new_pipes.append(pipe)
            
            pipe.draw(screen)
        
        pipes = new_pipes
        
        # Score display
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Check collision with ground or pipes
        if bird.y > HEIGHT - 50:
            return False, max(best_score, score)
        
        for pipe in pipes:
            if (bird.x - 40 < pipe.x + pipe.width and 
                bird.x + 40 > pipe.x and 
                (bird.y - 30 < pipe.height or bird.y + 30 > HEIGHT - pipe.gap - pipe.height)):
                return False, max(best_score, score)
        
        # Update screen
        pygame.display.flip()
        clock.tick(FPS)
    
    return True, best_score

# Main game loop
best = 0
while True:
    game_over, current_best = game()
    if not game_over:
        break
    
    # Show game over text
    font = pygame.font.Font(None, 74)
    game_text = font.render("Game Over", True, (255, 0, 0))
    best_text = font.render(f"Best: {current_best}", True, (255, 0, 0))
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.blit(game_text, (WIDTH//4, HEIGHT//3))
    screen.blit(best_text, (WIDTH//4, HEIGHT//3 + 64))
    pygame.display.flip()
    
    # Wait for space to restart or q to quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    best = current_best
                    break

# Quit Pygame
pygame.quit()
