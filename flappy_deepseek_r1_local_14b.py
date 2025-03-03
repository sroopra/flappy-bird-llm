import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 30

# Colors
LIGHT_COLORS = [(25, 194, 227), (255, 255, 255), (255, 255, 255)]
DARK_COLORS = [(0, 0, 0), (68, 132, 255), (149, 149, 149)]
BROWN_COLORS = [(139, 107, 43), (255, 215, 0)]

# Randomly choose background color
BACKGROUND_COLOR = random.choice(LIGHT_COLORS)

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.velocity = 0
        self.acceleration = -8
        self.gravity = 0.5
        
        # Randomly choose bird shape and color
        self.shapes = ['square', 'circle', 'triangle']
        self.shape = random.choice(self.shapes)
        self.color = random.choice(DARK_COLORS)
        
    def update(self):
        self.velocity += self.acceleration
        self.velocity *= 0.95
        self.y += self.velocity
        
        if self.y < 0:
            self.y = 0
            
    def draw(self):
        x = self.x
        y = self.y
        color = self.color
        
        if self.shape == 'square':
            pygame.draw.rect(screen, color, (x, y, 40, 40))
        elif self.shape == 'circle':
            pygame.draw.circle(screen, color, (int(x + 20), int(y + 20)), 20)
        elif self.shape == 'triangle':
            points = [(x, y), (x+40, y), (x+20, y-40)]
            pygame.draw.polygon(screen, color, points)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.width = 60
        self.height = random.randint(150, HEIGHT - 150)
        
        # Randomly choose pipe color
        self.color = random.choice([(0, 128, 0), (233, 196, 134), (128, 128, 128)])
        
    def update(self):
        self.x -= 5
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x, HEIGHT - self.height, self.width, HEIGHT))

def game_loop():
    # Initialize game objects
    bird = Bird()
    pipes = []
    score = 0
    best_score = 0
    running = True
    
    def generate_pipe():
        pipe = Pipe()
        pipes.append(pipe)
        
    # Game loop
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.velocity = -15  # Jump
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return
        
        # Update game objects
        bird.update()
        
        if len(pipes) == 0 or pipes[-1].x < WIDTH // 2:
            generate_pipe()
            
        for pipe in pipes:
            pipe.update()
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
                score += 1
                
                # Update best score
                if score > best_score:
                    best_score = score
        
        # Draw game objects
        bird.draw()
        
        for pipe in pipes:
            pipe.draw()
            
        # Draw land
        pygame.draw.rect(screen, random.choice(BROWN_COLORS), (0, HEIGHT - 50, WIDTH, 50))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (WIDTH - 100, 50))
        
        # Check collisions
        for pipe in pipes:
            if (bird.x < pipe.x + pipe.width and 
                bird.x + 40 > pipe.x and 
                (bird.y < pipe.height or bird.y + 40 > HEIGHT - pipe.height)):
                running = False
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    # Game over screen
    while True:
        screen.fill(BACKGROUND_COLOR)
        
        font = pygame.font.Font(None, 74)
        text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return
        
        pygame.display.flip()

# Start the game
game_loop()
