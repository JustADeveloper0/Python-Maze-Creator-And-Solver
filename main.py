import pygame
import sys
import random
from icecream import ic

pygame.init()

def manhattan_distance(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def astar(maze, start, end):
    open_set = set([start])
    closed_set = set()
    came_from = {}

    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, end)}
    extra = set()

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))

        if current == end:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return [path, extra]

        open_set.remove(current)
        closed_set.add(current)
        extra.add(current)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if neighbor in closed_set or maze[neighbor[0]][neighbor[1]] == 1:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in open_set or tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, end)
                open_set.add(neighbor)

    return None

def create_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def create_path(row, col):
        maze[row][col] = 0
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if 0 < new_row < rows and 0 < new_col < cols and maze[new_row][new_col] == 1:
                maze[row + dx // 2][col + dy // 2] = 0
                create_path(new_row, new_col)

    create_path(1, 1)
    maze[rows - 2][1] = 3  # Entrance
    exit = []
    done = False
    while done != True:
        r, c = random.randint(1, rows - 2), random.randint(1, cols - 2)
        if maze[r][c] != 1 or maze[r][c] != 3:
            exit = [r, c]
            done = True
    maze[exit[0]][exit[1]] = 2  # Exit
    return maze, [rows - 2, 1], exit


r, c = 49, 49 # only odd numbers for the values
values = create_maze(r, c)
start, end = values[1], values[2]
maze = values[0]

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = len(maze), len(maze[0])
TILE_SIZE = WIDTH // COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

for i, row in enumerate(maze):
    if i != len(maze):
        maze[i].append(1)
maze.append([1] * len(maze[0]))

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if maze[y][x] == 2:
                pygame.draw.rect(screen, (0, 255, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if maze[y][x] == 3:
                pygame.draw.rect(screen, (255, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def solve_maze():
    path = astar(maze, tuple(start), tuple(end))
    for position in path[1]:
        x, y = position[0], position[1]
        pygame.draw.rect(screen, (255, 165, 0), (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    for position in path[0]:
        x, y = position[0], position[1]
        pygame.draw.rect(screen, (128, 0, 128), (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def main():
    solve = False
    maze = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    solve = not solve
                if event.key == pygame.K_m:
                    maze = not maze
                if event.key == pygame.K_q:
                    solve = not solve
                    maze = not maze

        screen.fill(WHITE)
        if solve:
            solve_maze()
        if maze:
            draw_maze()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

