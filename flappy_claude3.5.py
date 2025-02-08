import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60
GRAVITY = 0.25
JUMP_SPEED = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1600  # milliseconds

# Colors
def get_random_light_color():
    return (random.randint(180, 255), random.randint(180, 255), random.randint(180, 255))

def get_random_dark_color():
    return (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))

# Initialize the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.reset()
        self.color = get_random_dark_color()
        self.shape = random.choice(['square', 'circle', 'triangle'])
        
    def reset(self):
        self.x = WINDOW_WIDTH // 4
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        
    def jump(self):
        self.velocity = JUMP_SPEED
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self, surface):
        if self.shape == 'square':
            pygame.draw.rect(surface, self.color, (self.x - 15, self.y - 15, 30, 30))
        elif self.shape == 'circle':
            pygame.draw.circle(surface, self.color, (self.x, self.y), 15)
        else:  # triangle
            points = [
                (self.x - 15, self.y + 15),
                (self.x + 15, self.y + 15),
                (self.x, self.y - 15)
            ]
            pygame.draw.polygon(surface, self.color, points)
            
    def get_mask(self):
        if self.shape == 'square':
            return pygame.Rect(self.x - 15, self.y - 15, 30, 30)
        elif self.shape == 'circle':
            return pygame.Rect(self.x - 15, self.y - 15, 30, 30)  # Simplified collision
        else:
            return pygame.Rect(self.x - 15, self.y - 15, 30, 30)  # Simplified collision

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, 400)
        self.color = random.choice([
            (0, 100, 0),  # Dark green
            (139, 69, 19),  # Brown
            (64, 64, 64)   # Dark gray
        ])
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, surface):
        # Bottom pipe
        pygame.draw.rect(surface, self.color,
                        (self.x - 30, self.height, 60, WINDOW_HEIGHT - self.height))
        # Top pipe
        pygame.draw.rect(surface, self.color,
                        (self.x - 30, 0, 60, self.height - PIPE_GAP))
        
    def collides_with(self, bird_mask):
        pipe_rects = [
            pygame.Rect(self.x - 30, 0, 60, self.height - PIPE_GAP),
            pygame.Rect(self.x - 30, self.height, 60, WINDOW_HEIGHT - self.height)
        ]
        return any(pipe_rect.colliderect(bird_mask) for pipe_rect in pipe_rects)

def main():
    bird = Bird()
    pipes = []
    score = 0
    best_score = 0
    last_pipe = pygame.time.get_ticks()
    game_active = True
    background_color = (173, 216, 230)  # Light blue
    ground_color = random.choice([(139, 69, 19), (218, 165, 32)])  # Dark brown or golden yellow
    
    font = pygame.font.Font(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key in (K_ESCAPE, K_q):
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    if game_active:
                        bird.jump()
                    else:
                        # Reset game
                        bird.reset()
                        pipes.clear()
                        score = 0
                        last_pipe = pygame.time.get_ticks()
                        game_active = True
                        background_color = get_random_light_color()
                        ground_color = random.choice([(139, 69, 19), (218, 165, 32)])
        
        screen.fill(background_color)
        
        if game_active:
            # Update bird
            bird.update()
            
            # Generate pipes
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe(WINDOW_WIDTH + 30))
                last_pipe = current_time
            
            # Update and draw pipes
            for pipe in pipes[:]:
                pipe.update()
                pipe.draw(screen)
                
                if pipe.x < -30:
                    pipes.remove(pipe)
                    continue
                
                if pipe.x < bird.x and not pipe.passed:
                    score += 1
                    pipe.passed = True
                
                if pipe.collides_with(bird.get_mask()):
                    game_active = False
                    best_score = max(score, best_score)
            
            # Check ground/ceiling collision
            if bird.y < 0 or bird.y > WINDOW_HEIGHT - 50:
                game_active = False
                best_score = max(score, best_score)
            
            bird.draw(screen)
            
            # Draw score
            score_text = font.render(f'Score: {score}', True, (0, 0, 0))
            screen.blit(score_text, (WINDOW_WIDTH - 120, 10))
        else:
            # Game over screen
            game_over_text = font.render('Game Over!', True, (0, 0, 0))
            score_text = font.render(f'Best Score: {best_score}', True, (0, 0, 0))
            restart_text = font.render('Press SPACE to restart', True, (0, 0, 0))
            
            screen.blit(game_over_text, 
                       (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                        WINDOW_HEIGHT // 2 - 60))
            screen.blit(score_text,
                       (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                        WINDOW_HEIGHT // 2))
            screen.blit(restart_text,
                       (WINDOW_WIDTH // 2 - restart_text.get_width() // 2,
                        WINDOW_HEIGHT // 2 + 60))
        
        # Draw ground
        pygame.draw.rect(screen, ground_color, (0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()