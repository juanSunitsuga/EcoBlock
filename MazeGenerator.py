import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 64
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EcoBlock Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Asset path
ASSETS_PATH = "assets/"

# Load images
grass_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "grass.png"), (TILE_SIZE, TILE_SIZE))
sidewalk_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "sidewalk.png"), (TILE_SIZE, TILE_SIZE))
house_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "house.png"), (TILE_SIZE, TILE_SIZE))
bin_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "trash-bin.png"), (TILE_SIZE, TILE_SIZE))
bot_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "trash-bot.png"), (TILE_SIZE, TILE_SIZE))

# Trash images
trash_images = [
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "plastic-bottle.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "plastic.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "eaten-apple.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "fishbone.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "battery.png"), (TILE_SIZE, TILE_SIZE))
]

# NPC types
npc_imgs = {
    "educated": pygame.transform.scale(pygame.image.load(ASSETS_PATH + "educated-npc.png"), (TILE_SIZE, TILE_SIZE)),
    "normal": pygame.transform.scale(pygame.image.load(ASSETS_PATH + "normal-npc.png"), (TILE_SIZE, TILE_SIZE)),
    "non-educated": pygame.transform.scale(pygame.image.load(ASSETS_PATH + "non-educated-npc.png"), (TILE_SIZE, TILE_SIZE))
}

# Tile types
tile_map = [["grass" for _ in range(COLS)] for _ in range(ROWS)]

class TrashBin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(bin_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))

# Maze generator
def generate_maze():
    global tile_map
    wall = 'w'
    cell = 'c'
    unvisited = 'u'

    maze = [[unvisited for _ in range(COLS)] for _ in range(ROWS)]

    # Randomize starting point
    start_x, start_y = random.randint(1, ROWS - 2), random.randint(1, COLS - 2)
    maze[start_x][start_y] = cell
    walls = [
        [start_x - 1, start_y],
        [start_x + 1, start_y],
        [start_x, start_y - 1],
        [start_x, start_y + 1]
    ]

    for wall in walls:
        maze[wall[0]][wall[1]] = 'w'

    while walls:
        rand_wall = random.choice(walls)
        walls.remove(rand_wall)

        x, y = rand_wall
        if maze[x][y] == 'w':
            neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]
            cells = [n for n in neighbors if 0 <= n[0] < ROWS and 0 <= n[1] < COLS and maze[n[0]][n[1]] == cell]

            if len(cells) == 1:
                maze[x][y] = cell
                for n in neighbors:
                    if 0 <= n[0] < ROWS and 0 <= n[1] < COLS and maze[n[0]][n[1]] == unvisited:
                        maze[n[0]][n[1]] = 'w'
                        walls.append(n)

    for i in range(ROWS):
        for j in range(COLS):
            tile_map[i][j] = 'sidewalk' if maze[i][j] == cell else 'grass'

# Generate maze
generate_maze()

# Place houses adjacent to sidewalks
def place_houses():
    for _ in range(3):  # Place 3 houses
        while True:
            x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if tile_map[y][x] == "sidewalk":
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    house_x, house_y = x + dx, y + dy
                    if 0 <= house_x < COLS and 0 <= house_y < ROWS and tile_map[house_y][house_x] == "grass":
                        tile_map[house_y][house_x] = "house"
                        break
                break

place_houses()

# Draw tile based on type
def draw_tile(x, y):
    tile_type = tile_map[y][x]
    if tile_type == "grass":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "sidewalk":
        screen.blit(sidewalk_img, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "house":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
        screen.blit(house_img, (x * TILE_SIZE, y * TILE_SIZE))

class Trash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = random.choice(trash_images)

    def draw(self):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

class Bot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, trash_list):
        if trash_list:
            target = trash_list[0]
            if self.x < target.x: self.x += 1
            elif self.x > target.x: self.x -= 1
            elif self.y < target.y: self.y += 1
            elif self.y > target.y: self.y -= 1

            # Collect trash
            if self.x == target.x and self.y == target.y:
                trash_list.remove(target)

    def draw(self):
        screen.blit(bot_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))

class NPC:
    def __init__(self, x, y, npc_type):
        self.x = x
        self.y = y
        self.direction = 1
        self.npc_type = npc_type
        self.image = npc_imgs[npc_type]

    def move(self, trash_list):
        self.x += self.direction
        if self.x >= COLS or self.x < 0 or tile_map[self.y][self.x] != "sidewalk":
            self.direction *= -1
            self.x += self.direction

        # Throw trash based on type
        if random.random() < 0.05:
            if self.npc_type == "non-educated":
                trash_list.append(Trash(self.x, self.y))
            elif self.npc_type == "normal" and random.random() < 0.5:
                trash_list.append(Trash(self.x, self.y))

    def draw(self):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

# Game state
trashes = []
bots = [Bot(0, 0)]
npcs = []

# Place NPCs on sidewalks
for _ in range(3):  # Place 3 NPCs
    while True:
        x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
        if tile_map[y][x] == "sidewalk":
            npc_type = random.choice(["educated", "normal", "non-educated"])
            npcs.append(NPC(x, y, npc_type))
            break

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for npc in npcs:
        npc.move(trashes)

    for bot in bots:
        bot.move(trashes)

    for y in range(ROWS):
        for x in range(COLS):
            draw_tile(x, y)

    for trash in trashes:
        trash.draw()
    for bot in bots:
        bot.draw()
    for npc in npcs:
        npc.draw()

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
sys.exit()