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
    "normal": {
        "idle": pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/Idle.png"), (TILE_SIZE, TILE_SIZE)),
        "walk": [
            pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
            pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
        ]
    },
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
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = 4  # pixels per frame
        self.prev_pos = None
        self.moving = False

    def move(self, trash_list):
        if self.moving:
            return  # wait until current movement finishes

        # Determine next position
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if tile_map[ny][nx] == "sidewalk" and (nx, ny) != self.prev_pos:
                    neighbors.append((nx, ny))

        if neighbors:
            target = trash_list[0] if trash_list else None
            if target:
                cur_dist = abs(self.x - target.x) + abs(self.y - target.y)
                closer_steps = [
                    (nx, ny) for (nx, ny) in neighbors
                    if abs(nx - target.x) + abs(ny - target.y) < cur_dist
                ]
                if closer_steps:
                    next_x, next_y = random.choice(closer_steps)
                else:
                    next_x, next_y = random.choice(neighbors)
            else:
                next_x, next_y = random.choice(neighbors)

            self.prev_pos = (self.x, self.y)
            self.x, self.y = next_x, next_y
            self.target_x = self.x * TILE_SIZE
            self.target_y = self.y * TILE_SIZE
            self.moving = True

    def update(self, trash_list):
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            if abs(dx) <= self.speed and abs(dy) <= self.speed:
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False
                # Check for trash pickup
                for t in trash_list:
                    if self.x == t.x and self.y == t.y:
                        trash_list.remove(t)
                        break
            else:
                self.pixel_x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
                self.pixel_y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

    def draw(self):
        screen.blit(bot_img, (self.pixel_x, self.pixel_y))

class NPC:
    def __init__(self, x, y, npc_type):
        self.x = x
        self.y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = 4
        self.prev_pos = None
        self.moving = False
        self.npc_type = npc_type

        # Animation
        self.anim_frame = 0
        self.anim_timer = 0
        self.frame_interval = 10

        self.image = self.get_image(idle=True)

    def get_image(self, idle=False):
        if self.npc_type == "normal":
            if idle:
                return npc_imgs["normal"]["idle"]
            else:
                return npc_imgs["normal"]["walk"][self.anim_frame % 2]
        else:
            return npc_imgs[self.npc_type]

    def move(self, trash_list):
        if self.moving:
            return

        def is_walkable(x, y):
            return (0 <= x < COLS and
                    0 <= y < ROWS and
                    tile_map[y][x] == "sidewalk")

        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = self.x + dx, self.y + dy
            if is_walkable(nx, ny) and (nx, ny) != self.prev_pos:
                neighbors.append((nx, ny))

        if neighbors:
            self.prev_pos = (self.x, self.y)
            self.x, self.y = random.choice(neighbors)
            self.target_x = self.x * TILE_SIZE
            self.target_y = self.y * TILE_SIZE
            self.moving = True

    def update(self):
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y

            if abs(dx) <= self.speed and abs(dy) <= self.speed:
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False
                if self.npc_type == "normal":
                    self.image = self.get_image(idle=True)
            else:
                self.pixel_x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
                self.pixel_y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

                # Animate faster
                if self.npc_type == "normal":
                    self.anim_timer += 1
                    if self.anim_timer >= self.frame_interval:
                        self.anim_frame = (self.anim_frame + 1) % 2
                        self.image = self.get_image(idle=False)
                        self.anim_timer = 0

    def draw(self):
        screen.blit(self.image, (self.pixel_x, self.pixel_y))
        
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
# Game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and update
    for npc in npcs:
        npc.move(trashes)
        npc.update()

    for bot in bots:
        bot.move(trashes)
        bot.update(trashes)

    # Draw everything
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
    clock.tick(30)  

pygame.quit()
sys.exit()