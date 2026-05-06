import pygame
import random
import sys

pygame.init()

# OKNO
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

# KOLORY
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

# SNAKE
snake = [(200,200)]
dir = (20, 0)

# JEDZENIE
food = (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))

score = 0

def draw_text(t, x, y):
    screen.blit(font.render(t, True, WHITE), (x,y))

running = True
while running:
    clock.tick(10)
    screen.fill(BLACK)

    # EVENTY
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP: dir = (0,-20)
            if e.key == pygame.K_DOWN: dir = (0,20)
            if e.key == pygame.K_LEFT: dir = (-20,0)
            if e.key == pygame.K_RIGHT: dir = (20,0)

    # RUCH
    head = (snake[0][0] + dir[0], snake[0][1] + dir[1])
    snake.insert(0, head)

    # JEDZENIE
    if head == food:
        food = (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))
        score += 1
    else:
        snake.pop()

    # KOLIZJA
    if head in snake[1:] or head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT:
        running = False

    # RYSOWANIE
    for s in snake:
        pygame.draw.rect(screen, GREEN, (*s, 20, 20))

    pygame.draw.rect(screen, RED, (*food, 20, 20))

    draw_text(f"Score: {score}", 10, 10)

    pygame.display.update()

pygame.quit()
sys.exit()
