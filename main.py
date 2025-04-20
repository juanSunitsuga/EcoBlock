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
bot_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "trash-bot.png"), (TILE_SIZE, TILE_SIZE))

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

npc_list = [
    {"name": "Normal NPC", "level": 10, "location": "Alley", "type": "normal", "upgrade_button": None},
    {"name": "Uneducated NPC 1", "level": 7, "location": "Street", "type": "non-educated", "upgrade_button": None},
    {"name": "Uneducated NPC 2", "level": 6, "location": "Square", "type": "non-educated", "upgrade_button": None},
]

tile_map = [["grass" for _ in range(COLS)] for _ in range(ROWS)]

class TrashBin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(bin_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))

def generate_maze():
    global tile_map, bins
    bins = []  # List to store trash bins
    try:
        with open("maze.txt", "r") as file:
            lines = file.readlines()
            # Dynamically resize tile_map based on the maze dimensions
            tile_map = [["grass" for _ in range(len(lines[0].strip().split()))] for _ in range(len(lines))]
            for i, line in enumerate(lines):
                for j, char in enumerate(line.strip().split()):
                    if char == 'c':  # 'c' represents a sidewalk
                        tile_map[i][j] = 'sidewalk'
                    elif char == 'w':  # 'w' represents grass
                        tile_map[i][j] = 'grass'
                    elif char == 'u':  # 'u' represents a trash bin
                        tile_map[i][j] = 'trash_bin'
                        bins.append(TrashBin(j, i))  # Add the trash bin to the list
    except FileNotFoundError:
        print("Error: maze.txt not found. Please ensure the file exists in the same directory.")
        sys.exit(1)

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

def place_trash_bins():
    bins = []
    for _ in range(3):  # Generate 3 random trash bins
        while True:
            x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if tile_map[y][x] == "grass":
                # Ensure the trash bin is adjacent to a sidewalk
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS and tile_map[ny][nx] == "sidewalk":
                        bins.append(TrashBin(x, y))
                        tile_map[y][x] = "trash_bin"  # Mark the tile as a trash bin
                        break
                else:
                    continue  # Retry if no adjacent sidewalk is found
                break
    return bins

# Generate trash bins
bins = place_trash_bins()

def draw_tile(x, y):
    tile_type = tile_map[y][x]
    if tile_type == "grass":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "sidewalk":
        screen.blit(sidewalk_img, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "house":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
        screen.blit(house_img, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "trash_bin":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
        screen.blit(bin_img, (x * TILE_SIZE, y * TILE_SIZE))

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
        self.speed = 4
        self.moving = False
        self.capacity = 5  # Maximum trash capacity
        self.current_trash = 0  # Current trash count

    def move(self, direction, is_walkable):
        if self.moving:
            return

        # Determine the next position based on the input direction
        if direction == "up":
            next_x, next_y = self.x, self.y - 1
        elif direction == "down":
            next_x, next_y = self.x, self.y + 1
        elif direction == "left":
            next_x, next_y = self.x - 1, self.y
        elif direction == "right":
            next_x, next_y = self.x + 1, self.y
        else:
            return  # Invalid direction

        # Check if the next position is walkable
        if is_walkable(next_x, next_y):
            self.prev_pos = (self.x, self.y)
            self.x, self.y = next_x, next_y
            self.target_x = self.x * TILE_SIZE
            self.target_y = self.y * TILE_SIZE
            self.moving = True

    def update(self, trash_list, bins):
        global money
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            if abs(dx) <= self.speed and abs(dy) <= self.speed:
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False

                # Check for trash at the current position and pick it up
                for trash in trash_list[:]:  # Use a copy of the list to avoid modification issues
                    if self.x == trash.x and self.y == trash.y:
                        if self.current_trash < self.capacity:
                            self.current_trash += 1
                            trash_list.remove(trash)

                # Check if standing on a trash bin
                for bin in bins:
                    if self.x == bin.x and self.y == bin.y and self.current_trash > 0:
                        money += self.current_trash  # Earn $1 per trash
                        self.current_trash = 0  # Empty the trash
            else:
                self.pixel_x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
                self.pixel_y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

    def draw(self):
        screen.blit(bot_img, (self.pixel_x, self.pixel_y))

class NPC:
    def __init__(self, x, y, npc_type):
        self.x, self.y = x, y
        self.npc_type = npc_type
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = 4
        self.prev_pos = None
        self.moving = False
        self.direction = "south"  # Default direction
        self.anim_frame = 0
        self.anim_timer = 0
        self.frame_interval = 6
        self.capacity = 3 if npc_type == "educated" else 0  # Educated NPCs have a capacity
        self.current_trash = 0  # Current trash count
        self.returning_to_bin = False  # Whether the NPC is returning to a trash bin
        
        # Initialize the image with the first frame of the default direction
        self.image = npc_imgs[npc_type]["walk"][self.direction][self.anim_frame]

    def get_image(self):
        if self.npc_type == "normal":
            return npc_imgs["normal"]["walk"][self.direction][self.anim_frame % 2]
        elif self.npc_type == "educated":
            return npc_imgs["educated"]["walk"][self.direction][self.anim_frame % 2]
        else:
            return npc_imgs["non-educated"]["walk"][self.direction][self.anim_frame % 2]

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

    def move(self, trash_list, bins):
        if self.moving:
            return

        def is_walkable(x, y):
            return 0 <= x < COLS and 0 <= y < ROWS and tile_map[y][x] in ["sidewalk", "trash_bin"]

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
                    money += self.current_trash  # Earn $1 per trash
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
                next_x, next_y = shortest_path[0]  # Take the first step in the path

                dx = next_x - self.x
                dy = next_y - self.y
                if dx == 1:
                    self.direction = "east"
                elif dx == -1:
                    self.direction = "west"
                elif dy == 1:
                    self.direction = "south"
                elif dy == -1:
                    self.direction = "north"

                self.prev_pos = (self.x, self.y)
                self.x, self.y = next_x, next_y
                
                

                # Pick up the trash if at the same position
                for trash in trash_list[:]:
                    if self.x == trash.x and self.y == trash.y:
                        if self.current_trash < self.capacity:
                            self.current_trash += 1
                            trash_list.remove(trash)

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

            dx = next_x - self.x
            dy = next_y - self.y
            if dx == 1:
                self.direction = "east"
            elif dx == -1:
                self.direction = "west"
            elif dy == 1:
                self.direction = "south"
            elif dy == -1:
                self.direction = "north"

            self.x, self.y = next_x, next_y
            self.target_x = self.x * TILE_SIZE
            self.target_y = self.y * TILE_SIZE
            self.moving = True

            # Educated NPC picks up trash at the new position
            if self.npc_type == "educated":
                for trash in trash_list[:]:  # Use a copy of the list to avoid modification issues
                    if self.x == trash.x and self.y == trash.y:
                        if self.current_trash < self.capacity:
                            self.current_trash += 1
                            trash_list.remove(trash)

                        # Check if capacity is full
                        if self.current_trash >= self.capacity:
                            self.returning_to_bin = True

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

                if self.npc_type in ["normal", "educated", "non-educated"]:
                    self.anim_timer += 1
                    if self.anim_timer >= self.frame_interval:
                        self.anim_frame = (self.anim_frame + 1) % 2
                        self.image = self.get_image()
                        self.anim_timer = 0

        elif self.npc_type in ["normal", "educated", "non-educated"]:
            self.image = self.get_image()


         # Throw trash based on type
        if random.random() < 0.02:
            if self.npc_type == "non-educated":
                trash_list.append(Trash(self.x, self.y))
            elif self.npc_type == "normal" and random.random() < 0.5:
                trash_list.append(Trash(self.x, self.y))

        return True

    def draw(self):
        screen.blit(self.image, (self.pixel_x, self.pixel_y))
        # Draw the capacity above the NPC
        if self.npc_type == "educated":
            font = pygame.font.SysFont(None, 24)
            capacity_text = f"{self.current_trash}/{self.capacity}"
            text_surface = font.render(capacity_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.pixel_x + TILE_SIZE // 2, self.pixel_y - 10))

# Game state
money = 0  # Initialize money to 0
capacity_upgrade_cost = 10  # Cost to upgrade capacity
speed_upgrade_cost = 15    # Cost to upgrade speed
trashes = []
bots = [Bot(1, 1)]
npcs = []

def generate_npc(npc_type):
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
            return NPC(x, y, npc_type)


for _ in range(1):
    npcs.append(generate_npc("non-educated"))

for _ in range(2):
    npcs.append(generate_npc("normal"))

# Game loop
clock = pygame.time.Clock()
FRAME_RATE = 30 # Set a consistent frame rate
running = True
player_bot = Bot(1, 1)  # Initialize the player-controlled bot
menu_button_rect = pygame.Rect(WIDTH - 150, 10, 140, 40)  # Button dimensions
menu_open = False  # Track whether the menu is open

def is_walkable(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS and tile_map[y][x] in ["sidewalk", "trash_bin"]

def draw_menu():
    # Draw a semi-transparent gray overlay on the background
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Allow transparency
    overlay.fill((50, 50, 50, 150))  # RGBA: Dark gray with 150 alpha (transparency)
    screen.blit(overlay, (0, 0))

    # Draw the menu background
    menu_width, menu_height = WIDTH - 200, HEIGHT - 200  # Slightly smaller menu size
    menu_bg_rect = pygame.Rect(100, 100, menu_width, menu_height)
    pygame.draw.rect(screen, (50, 50, 50), menu_bg_rect)  # Dark gray background
    pygame.draw.rect(screen, (255, 255, 255), menu_bg_rect, 2)  # White border

    font = pygame.font.SysFont(None, 24)

    # Draw the title
    title_text = font.render("NPC Menu", True, (255, 255, 255))  # White text
    screen.blit(title_text, (menu_bg_rect.x + menu_width // 2 - 50, menu_bg_rect.y + 20))  # Centered title

    # Draw NPC details and images
    y_offset = menu_bg_rect.y + 60
    for npc in npc_list:
        # Draw NPC image
        npc_image = npc_imgs[npc["type"]]["walk"]["south"][0]  # Use the south-facing image
        screen.blit(npc_image, (menu_bg_rect.x + 20, y_offset))  # Display image on the left

        # Draw NPC details
        npc_text = f"{npc['name']} (Lv. {npc['level']}) - {npc['location']}"
        npc_surface = font.render(npc_text, True, (255, 255, 255))  # White text
        screen.blit(npc_surface, (menu_bg_rect.x + 100, y_offset + 10))  # Display text next to the image

        # Draw upgrade button
        upgrade_button_rect = pygame.Rect(menu_bg_rect.x + menu_width - 170, y_offset, 150, 40)
        pygame.draw.rect(screen, (100, 200, 100), upgrade_button_rect)  # Green button
        upgrade_text = font.render("Upgrade", True, (0, 0, 0))  # Black text
        screen.blit(upgrade_text, (upgrade_button_rect.x + 20, upgrade_button_rect.y + 10))

        # Update the button rect in the NPC dictionary
        npc["upgrade_button"] = upgrade_button_rect
        y_offset += 80  # Move to the next NPC
            
def display_stats(money, bot_capacity, bot_current_trash):
    font = pygame.font.SysFont(None, 36)  # Font size 36
    # Display money
    money_text = f"Money: ${money}"
    money_surface = font.render(money_text, True, (0, 0, 0))  # Black text
    screen.blit(money_surface, (10, 10))  # Top-left corner

    # Display bot capacity
    capacity_text = f"Bot Capacity: {bot_current_trash}/{bot_capacity}"
    capacity_surface = font.render(capacity_text, True, (0, 0, 0))  # Black text
    screen.blit(capacity_surface, (10, 50))  # Below the money text

    # Display upgrade instructions at the bottom-left corner
    upgrade_text = f"[1] (${capacity_upgrade_cost}) to upgrade capacity"
    upgrade_surface = font.render(upgrade_text, True, (0, 0, 0))  # Black text
    screen.blit(upgrade_surface, (10, HEIGHT - 50))  # Bottom-left corner
    
    upgrade_text = f"[2] (${speed_upgrade_cost}) to upgrade speed"
    upgrade_surface = font.render(upgrade_text, True, (0, 0, 0))  # Black text
    screen.blit(upgrade_surface, (10, HEIGHT - 25))  # Bottom-left corner

def check_game_completion():
    if not trashes and all(npc["type"] == "educated" for npc in npc_list):
        font = pygame.font.SysFont(None, 48)
        win_text = font.render("Congratulations! All NPCs are educated!", True, (0, 255, 0))  # Green text
        screen.blit(win_text, (WIDTH // 2 - 300, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(5000)  # Wait for 5 seconds
        pygame.quit()
        sys.exit()

while running:
    # Handle player input for the bot
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_bot.move("up", is_walkable)
    elif keys[pygame.K_s]:
        player_bot.move("down", is_walkable)
    elif keys[pygame.K_a]:
        player_bot.move("left", is_walkable)
    elif keys[pygame.K_d]:
        player_bot.move("right", is_walkable)
    screen.fill(WHITE)

    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:  # Toggle the menu with the Tab key
                menu_open = not menu_open

            # Handle NPC upgrades
            if menu_open:
                for npc in npc_list:
                    if npc["upgrade_button"] and money >= 20:
                        money -= 20
                        npc["level"] += 1
                        if npc["type"] == "non-educated" and npc["level"] >= 10:
                            npc["type"] = "educated"

    # Draw the game world
    for y in range(ROWS):
        for x in range(COLS):
            draw_tile(x, y)

    for trash_bin in bins:
        trash_bin.draw()

    for trash in trashes:
        trash.draw()
    player_bot.draw()
    for npc in npcs:
        npc.draw()

    # Pause game logic if the menu is open
    if not menu_open:
        # Update NPCs and the bot
        for npc in npcs:
            npc.move(trashes, bins)
            npc.update(trashes)
        player_bot.update(trashes, bins)

        # Display money and bot capacity
        display_stats(money, player_bot.capacity, player_bot.current_trash)

        # Check for game completion
        check_game_completion()
    else:
        # Draw the NPC menu
        draw_menu()

    # Maintain a consistent frame rate
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()
sys.exit()