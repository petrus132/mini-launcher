import pygame
import socket
import threading
import json

pygame.init()

W,H = 700,450
screen = pygame.display.set_mode((W,H))
font = pygame.font.SysFont("arial",16)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",5555))

name = input("Nick: ")
client.send(name.encode())

player = {"x":100,"y":100}
players = {}
blocks = []
chat = []

VEL_Y = 0
GRAVITY = 0.6
on_ground = False

send_timer = 0
clock = pygame.time.Clock()


def recv():
    global players, blocks, chat
    while True:
        try:
            data = client.recv(4096).decode()
            if not data:
                continue

            msg = json.loads(data)

            players = msg.get("players",{})
            blocks = msg.get("blocks",[])
            chat = msg.get("chat",[])

        except:
            pass

threading.Thread(target=recv, daemon=True).start()


def send(data):
    try:
        client.send(json.dumps(data).encode())
    except:
        pass


run = True

while run:
    clock.tick(30)

    screen.fill((10,10,20))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    speed = 2

    if keys[pygame.K_a]:
        player["x"] -= speed
    if keys[pygame.K_d]:
        player["x"] += speed

    if keys[pygame.K_SPACE] and on_ground:
        VEL_Y = -10

    # PLACE BLOCK
    if keys[pygame.K_e]:
        send({"action":"block"})

    # BREAK BLOCK
    if keys[pygame.K_f]:
        send({"action":"break"})

    # GRAVITY
    VEL_Y += GRAVITY
    player["y"] += VEL_Y

    if player["y"] > 380:
        player["y"] = 380
        VEL_Y = 0
        on_ground = True
    else:
        on_ground = False

    send_timer += 1
    if send_timer >= 6:
        send({"x":player["x"],"y":player["y"]})
        send_timer = 0

    # PLAYERS
    for i in players:
        p = players[i]
        pygame.draw.rect(screen,(0,255,0),(p["x"],p["y"],40,40))
        screen.blit(font.render(p["name"],True,(255,255,255)),(p["x"],p["y"]-15))

    # BLOCKS (FAST RENDER)
    for b in blocks:
        pygame.draw.rect(screen,(100,100,255),(b["x"],b["y"],40,40))

    pygame.display.update()

pygame.quit()
