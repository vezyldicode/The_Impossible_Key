import customtkinter as ctk
import tkinter as tk
from random import choice

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
        self.draw_maze()

        # Bind keyboard events
        self.root.bind("<Up>", lambda event: self.move_player("up"))
        self.root.bind("<Down>", lambda event: self.move_player("down"))
        self.root.bind("<Left>", lambda event: self.move_player("left"))
        self.root.bind("<Right>", lambda event: self.move_player("right"))

    def generate_maze(self):
        maze = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Create a guaranteed path
        for i in range(self.grid_size):
            maze[i][0] = 0  # Path along the first column
        for j in range(1, self.grid_size):
            maze[self.grid_size - 1][j] = 0  # Path along the bottom row

        # Add random open spaces for multiple exits
        for _ in range(self.grid_size * 2):  # Adjust density of open spaces
            row = choice(range(self.grid_size))
            col = choice(range(self.grid_size))
            maze[row][col] = 0

        maze[0][0] = 0  # Start point
        maze[self.grid_size - 1][self.grid_size - 1] = 0  # End point
        return maze

    def draw_maze(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "black" if self.maze[row][col] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

        # Draw player
        self.player = self.canvas.create_oval(
            self.player_pos[1] * self.cell_size + 10,
            self.player_pos[0] * self.cell_size + 10,
            self.player_pos[1] * self.cell_size + self.cell_size - 10,
            self.player_pos[0] * self.cell_size + self.cell_size - 10,
            fill="blue"
        )

        # Draw exit
        self.canvas.create_rectangle(
            self.exit_pos[1] * self.cell_size,
            self.exit_pos[0] * self.cell_size,
            self.exit_pos[1] * self.cell_size + self.cell_size,
            self.exit_pos[0] * self.cell_size + self.cell_size,
            fill="green"
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

        # Update player position on canvas
        self.canvas.coords(
            self.player,
            self.player_pos[1] * self.cell_size + 10,
            self.player_pos[0] * self.cell_size + 10,
            self.player_pos[1] * self.cell_size + self.cell_size - 10,
            self.player_pos[0] * self.cell_size + self.cell_size - 10
        )

        # Check for win
        if self.player_pos == self.exit_pos:
            self.win_game()

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
