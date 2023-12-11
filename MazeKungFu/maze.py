import pygame
import random

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
START_COLOR = (0, 255, 0)  # Green
END_COLOR = (255, 0, 0)    # Red
PLAYER_COLOR = (0, 0, 255)  # Blue

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

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

def draw_maze(maze, player):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                color = BLACK
            else:
                if (y, x) == (0, 1):  # Start block
                    color = START_COLOR
                elif (y, x) == (height - 1, width - 2):  # End block
                    color = END_COLOR
                else:
                    color = WHITE
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Draw the player
    pygame.draw.rect(screen, PLAYER_COLOR, (player.x * cell_size, player.y * cell_size, cell_size, cell_size))

def main():
    maze = generate_maze(width, height)
    player = Player(0, 0)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.y > 0 and maze[player.y - 1][player.x] == 0:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN and player.y < height - 1 and maze[player.y + 1][player.x] == 0:
                    player.move(0, 1)
                elif event.key == pygame.K_LEFT and player.x > 0 and maze[player.y][player.x - 1] == 0:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT and player.x < width - 1 and maze[player.y][player.x + 1] == 0:
                    player.move(1, 0)

        screen.fill(WHITE)
        draw_maze(maze, player)
        pygame.display.flip()

        clock.tick(10)  # Control the frame rate

if __name__ == "__main__":
    main()
