import pygame
import random
from MazeGenerator import generateMaze as _generate_maze_from_file

# Constants
TILE_SIZE = 64
ROWS, COLS = None, None  # To be set after maze load

# Global state containers
tile_map = []
bins = []
trashes = []
npcs = []
money = 100000
capacity_upgrade_cost = 10
speed_upgrade_cost = 15

# --- Maze & Map Generation ---
def generate_maze(path="maze.txt"):
    global tile_map, ROWS, COLS
    try:
        lines = open(path).read().splitlines()
        ROWS, COLS = len(lines), len(lines[0].split())
        tile_map = [["grass" for _ in range(COLS)] for _ in range(ROWS)]
        for y, line in enumerate(lines):
            for x, char in enumerate(line.split()):
                tile_map[y][x] = 'sidewalk' if char == 'c' else 'grass'
        _generate_maze_from_file(path)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        pygame.quit()
        sys.exit(1)

def place_houses(count=10):
    for _ in range(count):
        while True:
            x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if tile_map[y][x] == "sidewalk":
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    house_x, house_y = x + dx, y + dy
                    if 0 <= house_x < COLS and 0 <= house_y < ROWS and tile_map[house_y][house_x] == "grass":
                        tile_map[house_y][house_x] = "house"
                        break
                break

def place_trash_bins(count=3):
    global bins
    for _ in range(count):
        while True:
            x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if tile_map[y][x] == "grass":
                # Ensure the trash bin is adjacent to a sidewalk
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS and tile_map[ny][nx] == "sidewalk":
                        bins.append(TrashBin(x, y))
                        tile_map[y][x] = "trash_bin"
                        break
                else:
                    continue  # Retry if no adjacent sidewalk is found
                break
    return bins

# --- Entities ---
class TrashBin:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Trash:
    def __init__(self, x, y, image):
        self.x, self.y = x, y
        self.image = image

class Bot:
    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = 4
        self.moving = False
        self.capacity = 5
        self.current_trash = 0

        # Animation
        self.direction = "south"
        self.anim_frame = 0
        self.anim_timer = 0
        self.frame_interval = 6
        self.images = images  # dict containing frames
        self.image = self.images["walk"][self.direction][self.anim_frame]

    def move(self, direction, is_walkable):
        if self.moving:
            return

        # Determine the next position based on the input direction
        if direction == "up":
            next_x, next_y = self.x, self.y - 1
            self.direction = "north"
        elif direction == "down":
            next_x, next_y = self.x, self.y + 1
            self.direction = "south"
        elif direction == "left":
            next_x, next_y = self.x - 1, self.y
            self.direction = "west"
        elif direction == "right":
            next_x, next_y = self.x + 1, self.y
            self.direction = "east"
        else:
            return  # Invalid direction

        # Check if the next position is walkable
        if is_walkable(next_x, next_y):
            self.x, self.y = next_x, next_y
            self.target_x = self.x * TILE_SIZE
            self.target_y = self.y * TILE_SIZE
            self.moving = True

    def update(self, trash_list, bin_list):
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

        # Update animation timer and frame
        self.anim_timer += 1
        if self.anim_timer >= self.frame_interval:
            self.anim_frame = (self.anim_frame + 1) % 2
            self.image = self.get_image()
            self.anim_timer = 0

class NPC:
    def __init__(self, x, y, npc_type, images):
        self.x = x
        self.y = y
        self.npc_type = npc_type
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = 3
        self.prev_pos = None
        self.moving = False
        self.capacity = 3 if npc_type == "educated" else 0
        self.current_trash = 0
        self.returning_to_bin = False
        self.images = images
        self.image = self.images["walk"]["south"][0]

    def bfs(self, start, target, is_walkable):
        """
        Perform Breadth-First Search (BFS) to find the shortest path to the target.
        :param start: Tuple (x, y) representing the starting position.
        :param target: Tuple (x, y) representing the target position.
        :param is_walkable: Function to check if a tile is walkable.
        :return: List of tuples representing the path to the target, or None if no path is found.
        """
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

        # Throw trash based on type
        if random.random() < 0.02:
            should_throw = False
            if self.npc_type == "non-educated":
                should_throw = True
            elif self.npc_type == "normal" and random.random() < 0.5:
                should_throw = True

            if should_throw:
                # Check if this tile is a trash bin
                is_bin_tile = any(bin.x == self.x and bin.y == self.y for bin in bins)

                # Only add trash if it's not thrown into a bin
                if not is_bin_tile:
                    trash_list.append(Trash(self.x, self.y))
