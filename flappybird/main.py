import pygame
import random
import sys

pygame.init()

# ===== OKNO =====
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# ===== KOLORY =====
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# ===== GRACZ =====
bird_x = 80
bird_y = HEIGHT // 2
bird_vel = 0
gravity = 0.5
jump = -8

bird_size = 20

# ===== RURY =====
pipe_width = 60
pipe_gap = 150
pipe_speed = 3

pipes = []

def new_pipe():
    height = random.randint(100, 400)
    return {"x": WIDTH, "height": height}

pipes.append(new_pipe())

# ===== SCORE =====
score = 0

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

# ===== GAME LOOP =====
running = True
while running:
    clock.tick(60)
    screen.fill(BLUE)

    # EVENTY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_vel = jump

    # FIZYKA
    bird_vel += gravity
    bird_y += bird_vel

    # RYSUJ PTAKA
    pygame.draw.rect(screen, YELLOW, (bird_x, int(bird_y), bird_size, bird_size))

    # RURY
    for pipe in pipes:
        pipe["x"] -= pipe_speed

        # górna
        pygame.draw.rect(screen, GREEN,
            (pipe["x"], 0, pipe_width, pipe["height"]))

        # dolna
        pygame.draw.rect(screen, GREEN,
            (pipe["x"], pipe["height"] + pipe_gap,
             pipe_width, HEIGHT))

        # kolizja
        if (bird_x < pipe["x"] + pipe_width and
            bird_x + bird_size > pipe["x"]):

            if (bird_y < pipe["height"] or
                bird_y + bird_size > pipe["height"] + pipe_gap):
                running = False

        # punkt
        if pipe["x"] + pipe_width == bird_x:
            score += 1

    # usuń stare rury
    if pipes[0]["x"] < -pipe_width:
        pipes.pop(0)
        pipes.append(new_pipe())

    # kolizja z ziemią
    if bird_y > HEIGHT or bird_y < 0:
        running = False

    # SCORE
    draw_text(f"Score: {score}", 10, 10)

    pygame.display.update()

pygame.quit()
sys.exit()
