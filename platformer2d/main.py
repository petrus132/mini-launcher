import pygame
import math,random
pygame.init()

WIDTH, HEIGHT = 1700, 1000
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

TILE = 50

# ================= LEVELS =================

level1 = [
"................................",
"........................#.......",
"........................#.....$.",
"................@.C..........###",
"..............######.......#....",
".*.....P1...p...........##......",
"#####...........................",
"................................",
"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"################################",
]

level2 = [
".*..............................",
".#...#..........................",
"................................",
"@@@@@@@@@@@..@..................",
"##############@.C...............",
"..............####..............",
".$........C.....................",
".#.......###....................",
"@@@#..@@@@@@#@@#@###@...@.......",
"################################",
]

level3 = [
"#.$.............................",
"######..........................",
"...........###....#......#......",
"................................",
"............................#...",
"............#....C...P1.....p...",
".......#.........#..............",
"..##............................",
"....#C..........................",
"....###.........................",
".........###....................",
"................P1.....p........",
"......................P1....p...",
"..................P1......p.....",
"................#...............",
".*....#....#....................",
"###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
"################################",
]
LEVELc = [
"..........................",
".................$........",
".......#..#...#.###.......",
"...#......................",
"..........................",
"#.........................",
"..........................",
"..#...C...................",
"......#...................",
"......##..................",
"......#....P....p.........",
"@@@@@@#...................",
"#######...........#.......",
"..............#...........",
"..........#...............",
"...*...#..................",
"..###.....................",

]
LEVEL4 = [
".........................#..................................",
"................$.............#.............................",
"................#..@..@.....................................",
"...................####...........#.........................",
".......................................#.....C..............",
".........................................########...........",
"..........................................#.......P.p.......",
"..........................................#.................",
"..........................................#.......P...p.....",
"..........................................#...#..#..........",
"..........................................#.#...............",
"..........................................#.................",
"..........................................#.................",
"..........................................##................",
".......................................#..#.#...............",
"..........................................#.....#...........",
"...................................#......#.................",
"...................#.P....p.......................#.........",
".............................####.............C.............",
"..............#.............................#####...........",
".*...................................#####..................",
".*...@...@.#.........................#####..................",
"############.........................#####..................",
"....................................@#####@.................",
"....................................#######.................",
]
leveld = [
    "..........................",
    "..*.......................",
    ".##.......................",
    "............P1.....p.......",
    "............P9.....p.......",
    "##########################",
    ]
LEVEL5 = [
"############################################################",
"#..........................................................#",
"#.$........................................................#",
"####.......................................................#",
"#.....#....................................................#",
"#.........#................................................#",
"#...............#..........................................#",
"#..........................................................#",
"#..................##......................................#",
"#.....................P5.................p.................#",
"#................................P8..................p.....#",
"#......................................................#...#",
"#..........................................................#",
"#.........................................................##",
"#..........................................................#",
"#....................................................@@...@#",
"#.................................................##########",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#...............................................#.#P1.....p#",
"#.................................................#........#",
"#.................................................#P2.....p#",
"#.................................................#........#",
"#.................................................#P3.....p#",
"#.................................................#........#",
"#.................................................#P4.....p#",
"#.................................................#...#....#",
"#.................................................#.......##",
"#.................................................#........#",
"#..........................................................#",
"#.......................................................#@@#",
"#.................................#....#P.........p...######",
"#.............#....#....#..@...............................#",
"#........P...p.............#####...........................#",
"#..*....#..................................................#",
"#.###......................................................#",
"#..........................................................#",
"#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#",
"############################################################",
]
LEVEL9 = [
".*...........",
"####.........",
"...........$.",
"..P..........",
".......p..###",
]
LEVEL67 = [
"...........................$.",
".............................",
"############...........P7...p",
"#*.........#.................",
"#................P4......p...",
"##....#....C.................",
"#..........#####.P3......p...",
"#..#.....#.#.................",
"#..........#.....P2......p...",
"#@@@@@@@@@@#.................",
"############.....P1......p...",
]



level_lista = [LEVEL67,LEVEL9,level1, level2, level3,LEVELc,LEVEL4,LEVEL5]
current_level_index = 0

# ================= LOAD LEVEL =================
def load_level(level):
    tiles = []
    moving_platforms = []
    spikes = []
    checkpoints = []
    goals = []
    spawn_x = 100
    spawn_y = 100

    for y, row in enumerate(level):
        for x, col in enumerate(row):
            if col == "#":
                tiles.append(pygame.Rect(x*TILE, y*TILE, TILE, TILE))
            elif col == "@":
                spikes.append(pygame.Rect(x*TILE, y*TILE, TILE, TILE))
            elif col == "C":
                checkpoints.append(pygame.Rect(x*TILE, y*TILE, TILE, TILE))
            elif col == "$":
                goals.append(pygame.Rect(x*TILE, y*TILE, TILE, TILE))
            elif col == "*":
                spawn_x = x*TILE
                spawn_y = y*TILE
            elif col == "P":
                delay = 0
                if x+1 < len(row) and row[x+1].isdigit():
                    delay = ((int(row[x+1]))*25)
                start_x = x * TILE
                start_y = y * TILE
                end_x = None
                end_y = None
                for px in range(x+1, len(row)):
                    if row[px] == "p":
                        end_x = px * TILE
                        end_y = y * TILE
                        break
                if end_x is not None:
                    rect = pygame.Rect(start_x, start_y, TILE*2, 30)
                    moving_platforms.append({
                        "rect": rect,
                        "start": (start_x, start_y),
                        "end": (end_x, end_y),
                        "delay": delay,
                        "timer": 0,
                        "direction": 1
                    })
    return tiles, moving_platforms, spikes, checkpoints, goals, spawn_x, spawn_y

tiles, moving_platforms, spikes, checkpoints, goals, spawn_x, spawn_y = load_level(level_lista[current_level_index])

# ================= GRACZ =================
player = pygame.Rect(spawn_x, spawn_y, 40, 50)

vel_x = 0
vel_y = 0

gravity = 0.5
jump_power = -11
max_speed = 5
acc = 0.4
friction = 0.2

coyote_time = 0.1
coyote_timer = 0
double_jump_available = True

dash_speed = 10
dash_time = 0
dash_duration = 0.15
dash_cooldown = 0
dash_cd_time = 0.5
can_dash_air = True

dash_dir_x = 0
dash_dir_y = 0

trail = []

camera_x = 0
camera_y = 0

death_count = 0
color_timer = 0

# ================= GAME LOOP =================
running = True
while running:

    if player.y > 2000:
        death_count += 1
        player.x = spawn_x
        player.y = spawn_y
        vel_x = 0
        vel_y = 0

    dt = clock.tick(60)/1000
    color_timer += 0.01

    r = int((math.sin(color_timer) + 1) * 127)
    g = int((math.sin(color_timer + 2) + 1) * 127)
    b = int((math.sin(color_timer + 4) + 1) * 127)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ===== RUCH =====
    if keys[pygame.K_a]: vel_x -= acc
    if keys[pygame.K_d]: vel_x += acc

    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        if vel_x > 0: vel_x -= friction
        elif vel_x < 0: vel_x += friction

    vel_x = max(-max_speed, min(max_speed, vel_x))

    # ===== DASH 4 KIERUNKI =====
    if keys[pygame.K_l] and dash_cooldown <= 0:
        if can_dash_air:
            dash_time = dash_duration
            dash_cooldown = dash_cd_time
            can_dash_air = False
            dash_dir_x = (keys[pygame.K_d] - keys[pygame.K_a])
            dash_dir_y = (keys[pygame.K_s] - keys[pygame.K_w])
            if dash_dir_x == 0 and dash_dir_y == 0:
                dash_dir_x = 1

    if dash_time > 0:
        vel_x = dash_speed * dash_dir_x
        vel_y = dash_speed * dash_dir_y
        dash_time -= dt

    dash_cooldown -= dt

    # ===== PLATFORM MOVE =====
    for p in moving_platforms:

        if p["timer"] < p["delay"]:
            p["timer"] += 1
            continue

        rect = p["rect"]
        sx, sy = p["start"]
        ex, ey = p["end"]

        speed = 2

        if p["direction"] == 1:
            if rect.x < ex:
                rect.x += speed
            else:
                p["direction"] = -1
        else:
            if rect.x > sx:
                rect.x -= speed
            else:
                p["direction"] = 1

    # ===== POZIOM X =====
    player.x += vel_x
    for tile in tiles + [p["rect"] for p in moving_platforms]:
        if player.colliderect(tile):
            if vel_x > 0: player.right = tile.left
            elif vel_x < 0: player.left = tile.right
            vel_x = 0

    # ===== GRAWITACJA =====
    vel_y += gravity
    player.y += vel_y
    on_ground = False

    for tile in tiles + [p["rect"] for p in moving_platforms]:
        if player.colliderect(tile):
            if vel_y > 0:
                player.bottom = tile.top
                vel_y = 0
                on_ground = True
            elif vel_y < 0:
                player.top = tile.bottom
                vel_y = 0

    if on_ground:
        coyote_timer = coyote_time
        double_jump_available = True
        can_dash_air = True
    else:
        coyote_timer -= dt

    if keys[pygame.K_SPACE]:
        if coyote_timer > 0:
            vel_y = jump_power
            coyote_timer = 0
        elif double_jump_available:
            vel_y = jump_power
            double_jump_available = False

    # ===== TRAIL =====
    trail.append((player.centerx, player.centery))
    if len(trail) > 100 :
        trail.pop(random.randint(0,10))

    # ===== CHECKPOINT =====
    for cp in checkpoints:
        if player.colliderect(cp):
            spawn_x = cp.x
            spawn_y = cp.y

    # ===== SPIKES =====
    for spike in spikes:
        if player.colliderect(spike):
            death_count += 1
            player.x = spawn_x
            player.y = spawn_y
            vel_x = 0
            vel_y = 0

    # ===== GOAL =====
    for goal in goals:
        if player.colliderect(goal):
            current_level_index += 1
            if current_level_index >= len(level_lista):
                print("WYGRANA 🔥")
                running = False
            else:
                tiles, moving_platforms, spikes, checkpoints, goals, spawn_x, spawn_y = load_level(level_lista[current_level_index])
                player.x = spawn_x
                player.y = spawn_y
                vel_x = 0
                vel_y = 0

    camera_x = player.centerx - WIDTH//2
    camera_y = player.centery - HEIGHT//2

    window.fill((r,g,b))

    # ===== TRAIL =====
    for pos in trail:
        pygame.draw.circle(window,(255,255,255),
            (pos[0]-camera_x,pos[1]-camera_y),5)

    # ===== TILES =====
    for tile in tiles:
        pygame.draw.rect(window,(80,80,80),
            pygame.Rect(tile.x-camera_x,tile.y-camera_y,TILE,TILE))

    # ===== MOVING PLATFORMS =====
    for p in moving_platforms:
        rect = p["rect"]
        pygame.draw.rect(window,(255,100,100),
            pygame.Rect(rect.x-camera_x,rect.y-camera_y,rect.width,rect.height))

        # ===== PODGLĄD TORU RUCHU PLATFORM =====
        sx, sy = p["start"]
        ex, ey = p["end"]
        pygame.draw.line(window, (255,255,255),
                         (sx - camera_x + TILE//2, sy - camera_y + TILE//2),
                         (ex - camera_x + TILE//2, ey - camera_y + TILE//2), 2)

    # ===== SPIKES =====
    for spike in spikes:
        x = spike.x - camera_x
        y = spike.y - camera_y
        points = [(x,y+TILE),(x+TILE//2,y),(x+TILE,y+TILE)]
        pygame.draw.polygon(window,(255,255,0),points)

    # ===== CHECKPOINTS =====
    for cp in checkpoints:
        pygame.draw.rect(window,(0,255,0),
            pygame.Rect(cp.x-camera_x,cp.y-camera_y,TILE,TILE))

    # ===== GOALS =====
    for goal in goals:
        pygame.draw.rect(window,(255,0,255),
            pygame.Rect(goal.x-camera_x,goal.y-camera_y,TILE,TILE))

    # ===== PLAYER =====
    pygame.draw.rect(window,(0,150,255),
        pygame.Rect(player.x-camera_x,player.y-camera_y,
                    player.width,player.height))

    text = font.render(f"Deaths: {death_count}", True, (255,255,255))
    window.blit(text,(20,20))

    pygame.display.flip()

pygame.quit()


