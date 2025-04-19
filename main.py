import pygame
import sys
import random
from MazeGenerator import generateMaze  # Import the generateMaze function

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

# Use the imported generateMaze function
def generate_maze():
    global tile_map
    maze = generateMaze(ROWS, COLS)  # Generate the maze using the imported function

    # Update the tile_map based on the generated maze
    for i in range(ROWS):
        for j in range(COLS):
            tile_map[i][j] = 'sidewalk' if maze[i][j] == 'c' else 'grass'

# Generate maze
generate_maze()

# Place houses adjacent to sidewalks
def place_houses():
    for _ in range(10):  # Place 10 houses
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
        self.prev_pos = None  # to help avoid immediate back‑and‑forth

    def move(self, trash_list):
        # 1) Gather all sidewalk neighbors (Down, Right, Up, Left)
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if tile_map[ny][nx] == "sidewalk" and (nx, ny) != self.prev_pos:
                    neighbors.append((nx, ny))

        # 2) Decide next step
        if neighbors:
            if trash_list:
                # target the first piece of trash
                target = trash_list[0]
                # compute current distance
                cur_dist = abs(self.x - target.x) + abs(self.y - target.y)

                # filter for neighbors that actually get us closer
                closer_steps = [
                    (nx, ny) for (nx, ny) in neighbors
                    if abs(nx - target.x) + abs(ny - target.y) < cur_dist
                ]

                if closer_steps:
                    # if we have one or more “closer” options, pick randomly among them
                    next_x, next_y = random.choice(closer_steps)
                else:
                    # otherwise wander randomly among all sidewalk neighbors
                    next_x, next_y = random.choice(neighbors)
            else:
                # no trash: pure random sidewalk wander
                next_x, next_y = random.choice(neighbors)

            # commit the move
            self.prev_pos = (self.x, self.y)
            self.x, self.y = next_x, next_y

            # 3) Collect trash if we landed on it
            if trash_list and self.x == target.x and self.y == target.y:
                trash_list.remove(target)

        # always return True so caller knows the Bot is still active
        return True

    def draw(self):
        screen.blit(bot_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))


class NPC:
    def __init__(self, x, y, npc_type):
        self.x, self.y = x, y
        self.npc_type = npc_type
        self.image = npc_imgs[npc_type]
        self.prev_pos = None

    def move(self, trash_list):
        def is_walkable(x, y):
            return (0 <= x < COLS and
                    0 <= y < ROWS and
                    tile_map[y][x] == "sidewalk")

        # Collect all valid neighbors
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Down, Right, Up, Left
            nx, ny = self.x + dx, self.y + dy
            if is_walkable(nx, ny) and (nx, ny) != self.prev_pos:
                neighbors.append((nx, ny))

        # Randomly pick a valid neighbor
        if neighbors:
            self.prev_pos = (self.x, self.y)
            self.x, self.y = random.choice(neighbors)

        # Trash logic unchanged
        if random.random() < 0.05:
            if self.npc_type == "non-educated":
                trash_list.append(Trash(self.x, self.y))
            elif self.npc_type == "normal" and random.random() < 0.5:
                trash_list.append(Trash(self.x, self.y))

        return True

    def draw(self):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))
        
# Game state
trashes = []
bots = [Bot(0, 0)]
npcs = []

# Place NPCs on the edges of the frame
def generate_npc():
    while True:
        # Randomly choose an edge: 0 = top, 1 = bottom, 2 = left, 3 = right
        edge = random.choice([0, 1, 2, 3])
        if edge == 0:  # Top edge
            x, y = random.randint(0, COLS - 1), 0
        elif edge == 1:  # Bottom edge
            x, y = random.randint(0, COLS - 1), ROWS - 1
        elif edge == 2:  # Left edge
            x, y = 0, random.randint(0, ROWS - 1)
        elif edge == 3:  # Right edge
            x, y = COLS - 1, random.randint(0, ROWS - 1)

        # Ensure the NPC spawns on a sidewalk
        if tile_map[y][x] == "sidewalk":
            npc_type = random.choice(["educated", "normal", "non-educated"])
            return NPC(x, y, npc_type)

# Generate initial NPCs
for _ in range(3):  # Place 3 NPCs
    npcs.append(generate_npc())

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update NPCs
    for npc in npcs[:]:
        if not npc.move(trashes):  # If NPC leaves the frame, remove it
            npcs.remove(npc)
            npcs.append(generate_npc())  # Generate a new NPC

    # Update bots
    for bot in bots:
        bot.move(trashes)

    # Draw tiles
    for y in range(ROWS):
        for x in range(COLS):
            draw_tile(x, y)

    # Draw game objects
    for trash in trashes:
        trash.draw()
    for bot in bots:
        bot.draw()
    for npc in npcs:
        npc.draw()

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
sys.exit()