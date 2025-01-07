import customtkinter as ctk
import tkinter as tk
from random import choice, shuffle
from PIL import Image, ImageTk
import os

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mind Maze")
        self.root.geometry("1000x600")

        # Configure grid dimensions
        self.grid_size = 10
        self.cell_size = 50

        # Maze map
        self.maze = self.generate_maze()
        
        # Player position
        self.player_pos = [0, 0]

        # Exit position
        self.exit_pos = [self.grid_size - 1, self.grid_size - 1]


        self.UI_setup()

        # Draw maze
        self.images = {}  # Store images for reuse
        self.load_and_resize_images()
        self.draw_maze()

        # Load animation frames
        self.animation_frames = {
            "up": self.load_animation_frames("Image\Maze\hero\walkup"),
            "down": self.load_animation_frames("Image\Maze\hero\walkdown"),
            "left": self.load_animation_frames("Image\Maze\hero\walkleft"),
            "right": self.load_animation_frames("Image\Maze\hero\walkright"),
        }

        # Keep track of visited cells
        self.visited_cells = set()
        self.visited_cells.add(tuple(self.player_pos))

        # Bind keyboard events
        self.is_moving = False
        self.root.bind("<Up>", lambda event: self.move_player("up"))
        self.root.bind("<Down>", lambda event: self.move_player("down"))
        self.root.bind("<Left>", lambda event: self.move_player("left"))
        self.root.bind("<Right>", lambda event: self.move_player("right"))

        self.fog_overlay = None
        # self.update_fog()

    def UI_setup(self):
        # Create canvas for the game
        self.canvas = ctk.CTkCanvas(self.root, width=self.grid_size * self.cell_size,
                                    height=self.grid_size * self.cell_size, bg="white")
        self.canvas.pack()


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

    def load_animation_frames(self, folder_path):
        """Load and resize animation frames from a given folder."""
        frames = []
        for file_name in sorted(os.listdir(folder_path)):
            if file_name.endswith(".png"):
                image = Image.open(os.path.join(folder_path, file_name))
                resized_image = image.resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(resized_image))
        return frames

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
        # Draw exit
        self.canvas.create_image(
            self.exit_pos[1] * self.cell_size + self.cell_size // 2,
            self.exit_pos[0] * self.cell_size + self.cell_size // 2,
            image=self.images["exit"]
        )
        # Draw player
        self.player = self.canvas.create_image(
            self.player_pos[1] * self.cell_size + self.cell_size // 2,
            self.player_pos[0] * self.cell_size + self.cell_size // 2,
            image=self.images["player"]
        )

        
    def update_fog(self):
        """Update the fog overlay to highlight only cells around the player."""
        if self.fog_overlay:
            self.canvas.delete(self.fog_overlay)

        fog_image = Image.new("RGBA", (self.grid_size * self.cell_size, self.grid_size * self.cell_size), (0, 0, 0, 255))
        highlight_radius = 1  # Radius of visible area in cells
        px, py = self.player_pos

        for dx in range(-highlight_radius, highlight_radius + 1):
            for dy in range(-highlight_radius, highlight_radius + 1):
                nx, ny = px + dx, py + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    x1 = ny * self.cell_size
                    y1 = nx * self.cell_size
                    for x in range(x1, x1 + self.cell_size):
                        for y in range(y1, y1 + self.cell_size):
                            fog_image.putpixel((x, y), (0, 0, 0, 0))

        fog_tk = ImageTk.PhotoImage(fog_image)
        self.fog_overlay = self.canvas.create_image(0, 0, image=fog_tk, anchor=tk.NW)
        self.canvas.image = fog_tk  # Keep a reference to avoid garbage collection

    def animate_player(self, direction, target_pos):
        """Animate the player moving in the given direction."""
        frames = self.animation_frames[direction]
        start_x = self.player_pos[1] * self.cell_size + self.cell_size // 2
        start_y = self.player_pos[0] * self.cell_size + self.cell_size // 2
        end_x = target_pos[1] * self.cell_size + self.cell_size // 2
        end_y = target_pos[0] * self.cell_size + self.cell_size // 2

        steps = len(frames)
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps

        for i, frame in enumerate(frames):
            self.canvas.itemconfig(self.player, image=frame)
            self.canvas.coords(
                self.player,
                start_x + dx * (i + 1),
                start_y + dy * (i + 1)
            )
            self.root.update()
            
            self.root.after(20)  # Delay between frames
            


    def move_player(self, direction):
        if self.is_moving:
            return
        
        row, col = self.player_pos

        if direction == "up" and row > 0 and self.maze[row - 1][col] == 0:
            target_pos = [row - 1, col]
        elif direction == "down" and row < self.grid_size - 1 and self.maze[row + 1][col] == 0:
            target_pos = [row + 1, col]
        elif direction == "left" and col > 0 and self.maze[row][col - 1] == 0:
            target_pos = [row, col - 1]
        elif direction == "right" and col < self.grid_size - 1 and self.maze[row][col + 1] == 0:
            target_pos = [row, col + 1]
        else:
            return
        self.is_moving = True
        # Animate the movement
        self.animate_player(direction, target_pos)

        # Update player position
        self.player_pos = target_pos
        self.update_fog()
        # Call on_enter_new_cell if the cell is new
        current_cell = tuple(self.player_pos)
        if current_cell not in self.visited_cells:
            self.on_enter_new_cell(current_cell)
            self.visited_cells.add(current_cell)

        # Check for win
        if self.player_pos == self.exit_pos:
            self.win_game()
        else:
            self.is_moving = False

    def on_enter_new_cell(self, cell):
        """Handle logic for entering a new cell."""
        print(f"Entered new cell: {cell}")

    def win_game(self):
        def replay_prompt():
            popup = tk.Toplevel(self.root)
            popup.title("Game Over")
            popup.geometry("300x150")
            popup_label = tk.Label(popup, text="You Win! Play Again?", font=("Arial", 14))
            popup_label.pack(pady=20)

            def replay():
                popup.destroy()
                self.reset_game()

            def quit_game():
                popup.destroy()
                self.root.destroy()

            replay_button = tk.Button(popup, text="Replay", command=replay)
            quit_button = tk.Button(popup, text="Quit", command=quit_game)
            replay_button.pack(side=tk.LEFT, padx=20, pady=10)
            quit_button.pack(side=tk.RIGHT, padx=20, pady=10)

        def animate_victory():
            victory_frames = self.load_animation_frames("Image\Maze\hero\winA")
            for frame in victory_frames:
                self.canvas.itemconfig(self.player, image=frame)
                self.root.update()
                self.root.after(100)

        # Stop player movement
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")

        # Show victory animation
        animate_victory()

        # Display replay prompt
        replay_prompt()

    def reset_game(self):
        """Reset the game to start again."""
        self.player_pos = [0, 0]
        self.visited_cells = set()
        self.visited_cells.add(tuple(self.player_pos))
        self.maze = self.generate_maze()
        self.canvas.delete("all")
        self.draw_maze()
        self.is_moving = False
        self.update_fog()
        self.root.bind("<Up>", lambda event: self.move_player("up"))
        self.root.bind("<Down>", lambda event: self.move_player("down"))
        self.root.bind("<Left>", lambda event: self.move_player("left"))
        self.root.bind("<Right>", lambda event: self.move_player("right"))

if __name__ == "__main__":
    root = ctk.CTk()
    game = MazeGame(root)
    root.mainloop()
