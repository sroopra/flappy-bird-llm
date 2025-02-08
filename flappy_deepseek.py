import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_FORCE = -10
PIPE_SPEED = -3
PIPE_GAP = 150
PIPE_FREQ = 1500
LAND_HEIGHT = 50

# Color definitions
DARK_BROWN = (101, 67, 33)
DARK_YELLOW = (153, 153, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_BROWN = (181, 101, 29)
DARK_GRAY = (64, 64, 64)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def random_light_color():
    return (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))

def random_dark_color():
    return (random.randint(0, 127), random.randint(0, 127), random.randint(0, 127))

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.color = random_dark_color()
        self.shape = random.choice(['square', 'circle', 'triangle'])
        self.size = 20
    
    def jump(self):
        self.velocity += JUMP_FORCE
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
            self.velocity = 0
    
    def draw(self, screen):
        if self.shape == 'square':
            rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
            pygame.draw.rect(screen, self.color, rect)
        elif self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size//2)
        elif self.shape == 'triangle':
            points = [
                (self.x, self.y - self.size//2),
                (self.x - self.size//2, self.y + self.size//2),
                (self.x + self.size//2, self.y + self.size//2)
            ]
            pygame.draw.polygon(screen, self.color, points)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60
        self.gap_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.bottom_y = self.gap_height + PIPE_GAP
        self.color = random.choice([DARK_GREEN, LIGHT_BROWN, DARK_GRAY])
        self.passed = False
    
    def update(self):
        self.x += PIPE_SPEED
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.gap_height))
        pygame.draw.rect(screen, self.color, (self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y))
    
    def get_rects(self):
        return (pygame.Rect(self.x, 0, self.width, self.gap_height),
                pygame.Rect(self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    best_score = 0

    # Game state variables
    game_active = False
    score = 0
    background_color = random_light_color()
    land_color = random.choice([DARK_BROWN, DARK_YELLOW])
    bird = Bird()
    pipes = []
    last_pipe_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.jump()
                elif event.key == pygame.K_SPACE and not game_active:
                    # Reset game
                    game_active = True
                    bird = Bird()
                    pipes = []
                    score = 0
                    background_color = random_light_color()
                    land_color = random.choice([DARK_BROWN, DARK_YELLOW])
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
        
        if game_active:
            # Update bird
            bird.update()

            # Generate new pipes
            if current_time - last_pipe_time > PIPE_FREQ:
                pipes.append(Pipe(SCREEN_WIDTH))
                last_pipe_time = current_time
            
            # Update pipes and check scoring
            for pipe in pipes:
                pipe.update()
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1
                    best_score = max(score, best_score)
            
            # Remove off-screen pipes
            pipes = [pipe for pipe in pipes if pipe.x > -pipe.width]

            # Collision detection
            bird_rect = bird.get_rect()
            collision = False
            # Ground collision
            if bird_rect.bottom >= SCREEN_HEIGHT - LAND_HEIGHT:
                collision = True
            # Pipe collision
            for pipe in pipes:
                top_rect, bottom_rect = pipe.get_rects()
                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                    collision = True
                    break
            if collision:
                game_active = False

        # Drawing
        screen.fill(background_color)
        
        if game_active:
            # Draw pipes
            for pipe in pipes:
                pipe.draw(screen)
            
            # Draw bird
            bird.draw(screen)
        else:
            # Game over text
            game_over_text = font.render("Game Over", True, BLACK)
            score_text = font.render(f"Score: {score}", True, BLACK)
            best_text = font.render(f"Best: {best_score}", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            screen.blit(best_text, (SCREEN_WIDTH//2 - best_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
        
        # Draw land and score
        pygame.draw.rect(screen, land_color, (0, SCREEN_HEIGHT - LAND_HEIGHT, SCREEN_WIDTH, LAND_HEIGHT))
        score_surface = font.render(str(score), True, BLACK)
        screen.blit(score_surface, (SCREEN_WIDTH - 50, 10))
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()