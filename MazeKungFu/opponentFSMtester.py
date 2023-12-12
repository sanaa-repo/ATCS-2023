import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of each cell and the size of the window
cell_size = 30
width, height = 21, 21
window_size = (width * cell_size, height * cell_size)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Maze Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def dfs(x, y):
        maze[y][x] = 0  # Mark the current cell as visited

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy  # Jump two steps
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0  # Carve a path
                dfs(nx, ny)

    # Start DFS from the top-left corner
    dfs(1, 1)

    # Place entrance at the top-left corner
    maze[0][1] = 0

    # Place exit at the bottom-right corner
    maze[height - 1][-2] = 0

    return maze

def draw_maze(maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = WHITE if cell == 0 else BLACK
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

def draw_player(player_pos):
    x, y = player_pos
    pygame.draw.circle(screen, RED, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2)

def main():
    maze = generate_maze(width, height)
    player_pos = (1, 0)  # Start the player at the entrance

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and maze[player_pos[1] - 1][player_pos[0]] == 0:
            player_pos = (player_pos[0], player_pos[1] - 1)
        elif keys[pygame.K_DOWN] and maze[player_pos[1] + 1][player_pos[0]] == 0:
            player_pos = (player_pos[0], player_pos[1] + 1)
        elif keys[pygame.K_LEFT] and maze[player_pos[1]][player_pos[0] - 1] == 0:
            player_pos = (player_pos[0] - 1, player_pos[1])
        elif keys[pygame.K_RIGHT] and maze[player_pos[1]][player_pos[0] + 1] == 0:
            player_pos = (player_pos[0] + 1, player_pos[1])

        screen.fill(BLACK)
        draw_maze(maze)
        draw_player(player_pos)

        # Mark the exit with a green circle
        pygame.draw.circle(screen, GREEN, ((width - 2) * cell_size + cell_size // 2, (height - 1) * cell_size + cell_size // 2), cell_size // 2)

        pygame.display.flip()

        if player_pos == (width - 2, height - 1):  # Player reached the exit
            print("Congratulations! You reached the exit.")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
