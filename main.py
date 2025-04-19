# -- existing imports and initializations --
import pygame
import sys
import random
from MazeGenerator import generateMaze  # Import the generateMaze function

pygame.init()

# Screen settings
WIDTH, HEIGHT = 832, 640
TILE_SIZE = 64
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EcoBlock Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ASSETS_PATH = "assets/"

# Load images
grass_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "grass.png"), (TILE_SIZE, TILE_SIZE))
sidewalk_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "sidewalk.png"), (TILE_SIZE, TILE_SIZE))
house_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "house.png"), (TILE_SIZE, TILE_SIZE))
bin_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "trash-bin.png"), (TILE_SIZE, TILE_SIZE))
# bot_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "trash-bot.png"), (TILE_SIZE, TILE_SIZE))

trash_images = [
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "plastic-bottle.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "plastic.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "eaten-apple.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "fishbone.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "battery.png"), (TILE_SIZE, TILE_SIZE))
]

# NPC types
npc_imgs = {
    "educated": {
        "walk": {
            "north": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "south": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "east": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "west": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
            ]
        }
    },
    "normal": {
        "walk": {
            "north": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "south": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "east": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "west": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
            ]
        }
    },
    "non-educated": {
        "walk": {
            "north": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "south": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "east": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "west": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
            ]
        }
    }
}


tile_map = [["grass" for _ in range(COLS)] for _ in range(ROWS)]

class TrashBin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(bin_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))

def generate_maze():
    global tile_map
    maze = generateMaze(ROWS, COLS)
    for i in range(ROWS):
        for j in range(COLS):
            tile_map[i][j] = 'sidewalk' if maze[i][j] == 'c' else 'grass'

generate_maze()

def place_houses():
    for _ in range(10):
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

def draw_tile(x, y):
    tile_type = tile_map[y][x]
    if tile_type == "grass" or tile_type == "trash_bin":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))  # Always draw grass first
        if tile_type == "trash_bin":
            screen.blit(bin_img, (x * TILE_SIZE, y * TILE_SIZE))  # Draw trash bin on top
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
        self.prev_pos = None
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = player_bot_speed
        self.moving = False
        self.inventory = []  # Stores collected trash

    def update(self, trash_list):
        global money
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            if abs(dx) <= self.speed and abs(dy) <= self.speed:
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False

                # Collect trash if on the same position
                for trash in trash_list[:]:
                    if self.x == trash.x and self.y == trash.y:
                        if len(self.inventory) < player_bot_capacity:
                            self.inventory.append(trash)
                            trash_list.remove(trash)

                # Check if standing on a trash bin
                for bin in bins:
                    if self.x == bin.x and self.y == bin.y and self.inventory:
                        money += len(self.inventory) * 10  # Earn money for collected trash
                        self.inventory.clear()
            else:
                self.pixel_x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
                self.pixel_y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

    def draw(self):
        # Draw the bot at its current position
        screen.blit(bot_img, (self.pixel_x, self.pixel_y))

class NPC:
    def __init__(self, x, y, npc_type):
        self.x = x
        self.y = y
        self.npc_type = npc_type
        self.image = npc_imgs[npc_type]["walk"]["south"][0]  # Default image
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = 4
        self.prev_pos = None
        self.moving = False
        self.direction = "south"
        self.anim_frame = 0
        self.anim_timer = 0
        self.frame_interval = 6
        self.capacity = 3  # Default capacity for educated NPCs
        self.current_trash = 0  # Current trash count
        self.returning_to_bin = False  # Whether the NPC is returning to a trash bin
        
    def bfs(self, start, target, is_walkable):
        """Perform BFS to find the shortest path to the target."""
        queue = [(start, [])]  # (current_position, path)
        visited = set()

        while queue:
            (current_x, current_y), path = queue.pop(0)
            if (current_x, current_y) in visited:
                continue
            visited.add((current_x, current_y))

            # If we reach the target, return the path
            if (current_x, current_y) == target:
                return path

            # Explore neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current_x + dx, current_y + dy
                if is_walkable(nx, ny) and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return None  # No path found
    
    def move(self, trash_list):
        if self.moving:
            return

        def is_walkable(x, y):
            return (0 <= x < COLS and 0 <= y < ROWS and tile_map[y][x] in ["sidewalk", "trash_bin"])

        # If returning to a trash bin
        if self.returning_to_bin:
            nearest_bin = None
            shortest_path = None
            for bin in bins:
                path = self.bfs((self.x, self.y), (bin.x, bin.y), is_walkable)
                if path and (shortest_path is None or len(path) < len(shortest_path)):
                    nearest_bin = bin
                    shortest_path = path

            if shortest_path:
                next_x, next_y = shortest_path[0]
                self.prev_pos = (self.x, self.y)
                self.x, self.y = next_x, next_y

                # Check if the NPC has reached the trash bin
                if self.x == nearest_bin.x and self.y == nearest_bin.y:
                    global money
                    money += self.current_trash  # Generate $1 per trash
                    self.current_trash = 0  # Empty the trash
                    self.returning_to_bin = False  # Resume collecting trash

                self.target_x = self.x * TILE_SIZE
                self.target_y = self.y * TILE_SIZE
                self.moving = True
                return

        # If the NPC is educated, use BFS to find the nearest trash
        if self.npc_type == "educated" and trash_list:
            nearest_trash = None
            shortest_path = None
            for trash in trash_list:
                path = self.bfs((self.x, self.y), (trash.x, trash.y), is_walkable)
                if path and (shortest_path is None or len(path) < len(shortest_path)):
                    nearest_trash = trash
                    shortest_path = path

            # If a path to trash is found, move toward it
            if shortest_path:
                next_x, next_y = shortest_path[0]
                self.prev_pos = (self.x, self.y)
                self.x, self.y = next_x, next_y

                # Pick up the trash if at the same position
                for trash in trash_list[:]:
                    if self.x == trash.x and self.y == trash.y:
                        trash_list.remove(trash)
                        self.current_trash += 1  # Increment trash count

                        # Check if capacity is full
                        if self.current_trash >= self.capacity:
                            self.returning_to_bin = True

                self.target_x = self.x * TILE_SIZE
                self.target_y = self.y * TILE_SIZE
                self.moving = True
                return

        # Random movement if no trash is found
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = self.x + dx, self.y + dy
            if is_walkable(nx, ny):
                neighbors.append((nx, ny))

        if neighbors:
            self.prev_pos = (self.x, self.y)
            next_x, next_y = random.choice(neighbors)
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
            else:
                self.pixel_x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
                self.pixel_y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

        # Throw trash for non-educated and normal NPCs
        if random.random() < 0.02:
            if self.npc_type == "non-educated":
                trash_list.append(Trash(self.x, self.y))
            elif self.npc_type == "normal" and random.random() < 0.5:
                trash_list.append(Trash(self.x, self.y))

    def draw(self):
        screen.blit(self.image, (self.pixel_x, self.pixel_y))


# Game state
money = 0
player_bot_capacity = 3  # Default capacity
player_bot_speed = 4  # Default speed
trashes = []
npcs = []
player_bot = Bot(1, 1) 

def generate_npc():
    while True:
        edge = random.choice([0, 1, 2, 3])
        if edge == 0:
            x, y = random.randint(0, COLS - 1), 0
        elif edge == 1:
            x, y = random.randint(0, COLS - 1), ROWS - 1
        elif edge == 2:
            x, y = 0, random.randint(0, ROWS - 1)
        else:
            x, y = COLS - 1, random.randint(0, ROWS - 1)

        if tile_map[y][x] == "sidewalk":
            if not any(npc.npc_type == "educated" for npc in npcs):
                npc_type = "educated"
            else:
                npc_type = random.choice(["educated", "normal", "non-educated"])
            return NPC(x, y, npc_type)


for _ in range(3):
    npcs.append(generate_npc())

# Game loop
clock = pygame.time.Clock()
running = True
player_bot = Bot(1, 1)  # Initialize the player-controlled bot

def is_walkable(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS and tile_map[y][x] == "sidewalk"

font = pygame.font.SysFont(None, 32)
def draw_text_with_outline(text, font, x, y, main_color, outline_color=(0, 0, 0)):
    outline_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in outline_offsets:
        outline_surface = font.render(text, True, outline_color)
        screen.blit(outline_surface, (x + dx, y + dy))
    text_surface = font.render(text, True, main_color)
    screen.blit(text_surface, (x, y))

def draw_ui():
    draw_text_with_outline(f"Money: ${money}", font, 10, 10, (255, 255, 0))
    draw_text_with_outline(f"Capacity: {player_bot_capacity} [1]", font, 10, 40, (255, 255, 255))
    draw_text_with_outline(f"Speed: {player_bot_speed} [2]", font, 10, 70, (255, 255, 255))



def place_trash_bins():
    bins = []
    for _ in range(2):  # Generate 2 trash bins
        while True:
            x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if tile_map[y][x] == "grass":  # Ensure the bin is placed on a grass tile
                bins.append(TrashBin(x, y))
                tile_map[y][x] = "trash_bin"  # Mark the tile as a trash bin
                break
    return bins

# Generate trash bins
bins = place_trash_bins()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input for the bot
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_bot.move("up", is_walkable)
    elif keys[pygame.K_DOWN]:
        player_bot.move("down", is_walkable)
    elif keys[pygame.K_LEFT]:
        player_bot.move("left", is_walkable)
    elif keys[pygame.K_RIGHT]:
        player_bot.move("right", is_walkable)

    # Update and draw NPCs
    for npc in npcs:
        npc.move(trashes)
        npc.update(trashes)

    # Update the player-controlled bot (but do not draw it)
    player_bot.update(trashes)

    # Draw the game world
    for y in range(ROWS):
        for x in range(COLS):
            draw_tile(x, y)

    # Draw trash bins
    for trash_bin in bins:
        trash_bin.draw()

    # Draw other game objects
    for trash in trashes:
        trash.draw()
    for npc in npcs:
        npc.draw()

    # Tombol Upgrade    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1] and money >= 30:
        player_bot_capacity += 1
        money -= 30
    if keys[pygame.K_2] and money >= 50:
        player_bot_speed += 1
        money -= 50
        player_bot.speed = player_bot_speed

    draw_ui()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
# End of the code