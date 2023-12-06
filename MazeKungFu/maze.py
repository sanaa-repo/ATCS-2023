import random

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

def print_maze(maze):
    for row in maze:
        print(" ".join(["#" if cell == 1 else " " for cell in row]))

width, height = 15, 15 
maze = generate_maze(width, height)
print_maze(maze)
