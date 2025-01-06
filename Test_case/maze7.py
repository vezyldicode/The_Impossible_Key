import customtkinter as ctk
import tkinter as tk
from random import choice, shuffle
from PIL import Image, ImageTk

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game")
        self.root.geometry("600x600")

        # Configure grid dimensions
        self.grid_size = 10
        self.cell_size = 50

        # Maze map
        self.maze = self.generate_maze()
        
        # Player position
        self.player_pos = [0, 0]

        # Exit position
        self.exit_pos = [self.grid_size - 1, self.grid_size - 1]

        # Create canvas for the game
        self.canvas = ctk.CTkCanvas(self.root, width=self.grid_size * self.cell_size,
                                    height=self.grid_size * self.cell_size, bg="white")
        self.canvas.pack()

        # Draw maze
        self.images = {}  # Store images for reuse
        self.load_and_resize_images()
        self.draw_maze()

        # Keep track of visited cells
        self.visited_cells = set()
        self.visited_cells.add(tuple(self.player_pos))

        # Bind keyboard events
        self.root.bind("<Up>", lambda event: self.move_player("up"))
        self.root.bind("<Down>", lambda event: self.move_player("down"))
        self.root.bind("<Left>", lambda event: self.move_player("left"))
        self.root.bind("<Right>", lambda event: self.move_player("right"))

    def generate_maze(self):
        maze = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Create a guaranteed path using depth-first search (DFS)
        def carve_path(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and maze[nx][ny] == 1:
                    # Check for surrounding walls
                    surrounding_walls = sum(
                        1 for ddx, ddy in directions if 0 <= nx + ddx < self.grid_size and 0 <= ny + ddy < self.grid_size and maze[nx + ddx][ny + ddy] == 0
                    )
                    if surrounding_walls < 2:
                        maze[nx][ny] = 0
                        carve_path(nx, ny)

        # Start carving from the top-left corner
        maze[0][0] = 0
        carve_path(0, 0)

        # Ensure the bottom-right corner is reachable
        maze[self.grid_size - 1][self.grid_size - 1] = 0

        # Add random open spaces for variety and multiple paths
        for _ in range(self.grid_size * 3):
            row = choice(range(self.grid_size))
            col = choice(range(self.grid_size))
            maze[row][col] = 0

        return maze

    def load_and_resize_images(self):
        """Load and resize images to match the cell size."""
        def load_image(file_path):
            image = Image.open(file_path)
            resized_image = image.resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_image)

        self.images["wall"] = load_image("Image\Maze\level\wallStone.png")
        self.images["player"] = load_image("Image\Maze\hero\hitA\hero_hitA_0000.png")
        self.images["exit"] = load_image("Image\Maze\level\groundExit.png")
        self.images["path"] = load_image("Image\Maze\level\groundEarth_checkered.png")

    def draw_maze(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x_center = x1 + self.cell_size // 2
                y_center = y1 + self.cell_size // 2

                if self.maze[row][col] == 1:
                    self.canvas.create_image(x_center, y_center, image=self.images["wall"])
                else:
                    self.canvas.create_image(x_center, y_center, image=self.images["path"])

        # Draw player
        self.player = self.canvas.create_image(
            self.player_pos[1] * self.cell_size + self.cell_size // 2,
            self.player_pos[0] * self.cell_size + self.cell_size // 2,
            image=self.images["player"]
        )

        # Draw exit
        self.canvas.create_image(
            self.exit_pos[1] * self.cell_size + self.cell_size // 2,
            self.exit_pos[0] * self.cell_size + self.cell_size // 2,
            image=self.images["exit"]
        )

    def move_player(self, direction):
        row, col = self.player_pos

        if direction == "up" and row > 0 and self.maze[row - 1][col] == 0:
            self.player_pos[0] -= 1
        elif direction == "down" and row < self.grid_size - 1 and self.maze[row + 1][col] == 0:
            self.player_pos[0] += 1
        elif direction == "left" and col > 0 and self.maze[row][col - 1] == 0:
            self.player_pos[1] -= 1
        elif direction == "right" and col < self.grid_size - 1 and self.maze[row][col + 1] == 0:
            self.player_pos[1] += 1
        else:
            return

        # Update player position on canvas
        self.canvas.coords(
            self.player,
            self.player_pos[1] * self.cell_size + self.cell_size // 2,
            self.player_pos[0] * self.cell_size + self.cell_size // 2
        )

        # Call on_enter_new_cell if the cell is new
        current_cell = tuple(self.player_pos)
        if current_cell not in self.visited_cells:
            self.on_enter_new_cell(current_cell)
            self.visited_cells.add(current_cell)

        # Check for win
        if self.player_pos == self.exit_pos:
            self.win_game()

    def on_enter_new_cell(self, cell):
        """Handle logic for entering a new cell."""
        print(f"Entered new cell: {cell}")

    def win_game(self):
        self.canvas.create_text(
            self.grid_size * self.cell_size // 2,
            self.grid_size * self.cell_size // 2,
            text="You Win!",
            font=("Arial", 24),
            fill="red"
        )
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")

if __name__ == "__main__":
    root = ctk.CTk()
    game = MazeGame(root)
    root.mainloop()
