# https://github.com/OrWestSide/python-scripts
# Maze generator -- Randomized Prim Algorithm

## Imports
import random

# Constants
TILE_SIZE = 64
WIDTH, HEIGHT = 832, 640
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

wall = 'w'
cell = 'c'
unvisited = 'u'

# Save the maze to a file
def save_maze_to_file(maze, filename):
    with open(filename, 'w') as file:
        for row in maze:
            file.write(' '.join(row) + '\n')

# Find number of surrounding cells
def surroundingCells(maze, rand_wall):
    s_cells = 0
    if maze[rand_wall[0] - 1][rand_wall[1]] == cell:
        s_cells += 1
    if maze[rand_wall[0] + 1][rand_wall[1]] == cell:
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] - 1] == cell:
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] + 1] == cell:
        s_cells += 1
    return s_cells

# Maze generation function
def generateMaze(height, width):
    maze = [[unvisited for _ in range(width)] for _ in range(height)]

    # Randomize starting point
    start_x, start_y = random.randint(1, height - 2), random.randint(1, width - 2)
    maze[start_x][start_y] = cell
    walls = [
        [start_x - 1, start_y],
        [start_x + 1, start_y],
        [start_x, start_y - 1],
        [start_x, start_y + 1]
    ]

    for wall_pos in walls:
        maze[wall_pos[0]][wall_pos[1]] = wall

    while walls:
        rand_wall = random.choice(walls)
        walls.remove(rand_wall)

        x, y = rand_wall
        if maze[x][y] == wall:
            neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]
            cells = [n for n in neighbors if 0 <= n[0] < height and 0 <= n[1] < width and maze[n[0]][n[1]] == cell]

            if len(cells) == 1:
                maze[x][y] = cell
                for n in neighbors:
                    if 0 <= n[0] < height and 0 <= n[1] < width and maze[n[0]][n[1]] == unvisited:
                        maze[n[0]][n[1]] = wall
                        walls.append(n)

    return maze

# Main execution
if __name__ == "__main__":
    maze = generateMaze(ROWS, COLS)
    save_maze_to_file(maze, "maze.txt")  # Save the maze to a file
    print("Maze saved to maze.txt")