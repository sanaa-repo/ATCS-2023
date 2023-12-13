import pygame
import random
import sys
import time
from dojo_game import dojo_game
class MazeGame:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.window_size = (width * cell_size, height * cell_size)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Maze Game")

        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.maze = self.generate_maze(width, height)
        self.player_pos = (1, 0)  # Start the player at the entrance

        self.game = dojo_game()

        self.on_blue_block = False  # Track whether the player is on the blue block
        self.pink_screen_timer = 0  # Timer for displaying the pink screen


    def generate_maze(self, width, height):
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

        # Choose four random white blocks and replace them with blue blocks
        white_blocks = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == 0]
        if len(white_blocks) >= 4:
            for _ in range(2):#Note to self: Change num blue blocks here
                bx, by = random.choice(white_blocks)
                maze[by][bx] = 2  # Blue block
                white_blocks.remove((bx, by))

        return maze

    def draw_maze(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 0:
                    color = self.WHITE
                elif cell == 2:
                    color = self.BLUE
                else:
                    color = self.BLACK
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def draw_player(self):
        x, y = self.player_pos
        pygame.draw.circle(self.screen, self.RED, (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 2)

    def draw_exit(self):
        pygame.draw.circle(self.screen, self.GREEN, ((self.width - 2) * self.cell_size + self.cell_size // 2, (self.height - 1) * self.cell_size + self.cell_size // 2), self.cell_size // 2)

    def run(self):
        reached_exit = False
        while not reached_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP] and self.maze[self.player_pos[1] - 1][self.player_pos[0]] in {0, 2}:
                        self.player_pos = (self.player_pos[0], self.player_pos[1] - 1)
                    elif keys[pygame.K_DOWN] and self.maze[self.player_pos[1] + 1][self.player_pos[0]] in {0, 2}:
                        self.player_pos = (self.player_pos[0], self.player_pos[1] + 1)
                    elif keys[pygame.K_LEFT] and self.maze[self.player_pos[1]][self.player_pos[0] - 1] in {0, 2}:
                        self.player_pos = (self.player_pos[0] - 1, self.player_pos[1])
                    elif keys[pygame.K_RIGHT] and self.maze[self.player_pos[1]][self.player_pos[0] + 1] in {0, 2}:
                        self.player_pos = (self.player_pos[0] + 1, self.player_pos[1])

                    # Check if the player is on the blue block
                    self.on_blue_block = self.maze[self.player_pos[1]][self.player_pos[0]] == 2

            self.screen.fill(self.BLACK)
            self.draw_maze()
            self.draw_player()
            self.draw_exit()

            # Display pink screen for 2 seconds if the player is on the blue block
            if self.on_blue_block:
                self.game.run()
                self.pink_screen_timer += 1
                if self.pink_screen_timer >= 120:  # 2 seconds (assuming 60 FPS)
                    self.on_blue_block = False
                    self.pink_screen_timer = 0

            pygame.display.flip()

            if self.player_pos == (self.width - 2, self.height - 1):  # Player reached the exit
                print("Congratulations! You reached the exit.")
                reached_exit = True

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    game = MazeGame(21, 21, 30)
    game.run()
