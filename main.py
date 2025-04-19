import pygame
import sys

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
GREEN = (0, 200, 0)
BLUE = (50, 50, 255)
BROWN = (139, 69, 19)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

# Load images or use placeholder rectangles
def draw_tile(x, y, color):
    pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

class TrashBin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        draw_tile(self.x, self.y, BLUE)

class Trash:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        draw_tile(self.x, self.y, BROWN)

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
        draw_tile(self.x, self.y, GREEN)

# Game state
trash_bins = [TrashBin(5, 5), TrashBin(2, 2)]
trashes = [Trash(3, 3), Trash(6, 1)]
bots = [Bot(0, 0)]

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bot in bots:
        bot.move(trashes)

    for y in range(ROWS):
        for x in range(COLS):
            draw_tile(x, y, WHITE)

    for bin in trash_bins:
        bin.draw()
    for trash in trashes:
        trash.draw()
    for bot in bots:
        bot.draw()

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
sys.exit()
