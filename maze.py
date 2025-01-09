import customtkinter as ctk
import tkinter as tk
from random import choice, shuffle
from PIL import Image, ImageTk
import os
import random
from random import choice, shuffle, seed
from assets.quizzes.Rules_Dictionary import *
import time
from threading import Thread

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mind Maze")
        self.root.geometry("1000x800")
        self.configfile_path = "config\world_config.ini"
        self.anticheat = True

        # Configure grid dimensions
        self.grid_size = int(self.fsreach(self.configfile_path, "grid_size")) 
        self.cell_size = int(self.fsreach(self.configfile_path, "cell_size")) 

        # Seed for maze generation
        self.seed_input = 550871

        # Generate or set seed
        self.initialize_seed()

        # Maze map
        self.maze = self.generate_maze()
        self.is_Wingame = False
        
        # Player position
        self.player_pos = [0, 0]

        # Exit position
        self.exit_pos = [self.grid_size - 1, self.grid_size - 1]

        # Create main frame
        self.bg = self.fsreach(self.configfile_path, "background_color")
        self.textcolor = self.fsreach(self.configfile_path, "text_color")
        self.wrongcolor = self.fsreach(self.configfile_path, "wrong_color")
        self.textfont_family = self.fsreach(self.configfile_path, "text_font")
        self.textsize = int(self.fsreach(self.configfile_path, "text_size"))
        self.textfont = (self.textfont_family, self.textsize)


        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.bg)
        self.main_frame.pack(fill="both", expand=True)

        self.nav_bar = ctk.CTkFrame(self.main_frame,
                                    height=35)
        self.nav_bar.pack(padx =5, pady =5, fill='x')

        self.maze_frame = ctk.CTkFrame(self.main_frame,)
        self.maze_frame.pack(padx = 20, pady = 20,  side = "left", fill = "both")

        self.quizzes_frame = ctk.CTkFrame(self.main_frame)
        self.quizzes_frame.pack(padx = 20, pady = 20, side = "right", fill = "both", expand = "true")


        # Generate rules
        self.initialize_rules()

        self.UI_setup()

        # Draw maze
        self.images = {}  # Store images for reuse
        self.load_and_resize_images()
        self.draw_maze()

        # Load animation frames

        self.animation_frames = {
            "up": self.load_animation_frames("assets\hero\walkup"),
            "down": self.load_animation_frames("assets\hero\walkdown"),
            "left": self.load_animation_frames("assets\hero\walkleft"),
            "right": self.load_animation_frames("assets\hero\walkright"),
        }

        # Keep track of visited cells
        self.visited_cells = set()
        self.visited_cells.add(tuple(self.player_pos))

        # Bind keyboard events
        self.is_moving = False
        self.allows_move_player()
        # Create fog overlay
        self.fog_overlay = None
        self.update_fog()

        self.setting_tab()
        self.create_rule_label(1)
        self.running = True
        self.reset_event = False
        self.elapsed_time = 0
        thread = Thread(target=self.update_timer, daemon=True)
        thread.start()
    def UI_setup(self):
        self.setting_button = ctk.CTkButton(self.nav_bar,
                                text = "",
                                font=('Comic Sans MS', 15),
                                corner_radius=32,
                                command=self.open_settings,
                                width = 30)
        self.setting_button.pack(side="right", padx=10, pady=10)

        self.timer_label = ctk.CTkLabel(self.nav_bar,
                                text="00:00:00:00",
                                font=self.textfont)
        self.timer_label.pack(side="left")
        # Tạo canvas cho maze
        self.maze_canvas = ctk.CTkCanvas(self.maze_frame,
                                    width=self.grid_size * self.cell_size,
                                    height=self.grid_size * self.cell_size,
                                    bg=self.bg)
        self.maze_canvas.pack(anchor = "center")
        self.maze_canvas.bind("<Button-1>", self.allows_move_player)

        self.label_title = ctk.CTkLabel(
            self.quizzes_frame,
            text="Write down your password",
            font=self.textfont,
            justify="center",
            text_color=self.textcolor,)
        self.label_title.pack(padx=20, pady=20, anchor="center")

        self.userinput = ctk.CTkEntry(
            self.quizzes_frame,
            placeholder_text="Write Here",
            font=('Cascadia Mono', 18),
            fg_color='#F4F4F4',
            text_color='black',
            height=40,
            corner_radius=10
        )
        self.userinput.pack(padx=20, pady=12, anchor="center", fill="x")
        self.userinput.bind("<KeyRelease>", self.check_password)

        self.rules_frame = ctk.CTkScrollableFrame(self.quizzes_frame)
        self.rules_frame.pack(padx=20, pady=12, fill="both", expand=True)
        # self.userinput.bind("<KeyRelease>", self.password_change)

    def setting_tab(self):
        
        # Create settings frame
        self.settings_frame = ctk.CTkFrame(self.root, fg_color=self.bg)
        self.setting_nav_bar = ctk.CTkFrame(self.settings_frame,
                                        height=35)
        self.setting_nav_bar.pack(padx =5, pady =5, fill='x')

        # Back button in settings
        self.back_button = ctk.CTkButton(self.setting_nav_bar,
                                        text="Back",
                                        command=self.close_settings)
        self.back_button.pack(side="right", padx=10, pady=10)

        self.seed_label = ctk.CTkLabel(self.settings_frame,
                                        text=("Seed:"),
                                        font=self.textfont, 
                                        text_color=self.textcolor)
        self.seed_label.pack(side="left", padx=(20, 10), anchor = "n")
        self.seed_label.bind("<Button-1>", lambda event: (root.clipboard_clear(), root.clipboard_append(str(getattr(self, 'maze_seed')))))
        self.seed_entry = ctk.CTkEntry(self.settings_frame,
                                       width=200,
                                       border_width=0,
                                       font=self.textfont,
                                       text_color=self.textcolor,
                                       fg_color="transparent")
        self.seed_entry.pack(side="left", anchor = "n")

        self.checkbox = ctk.CTkCheckBox(self.settings_frame, text = "Option", font=self.textfont, 
                                        text_color=self.textcolor)
        self.checkbox.pack(side ="top", padx = 20, anchor = "w")

        self.update_setting()

    def update_setting(self):
            self.seed_label.configure(text="Seed:")
            self.seed_entry.delete(0, 'end')
            self.seed_entry.insert(0, self.maze_seed)

    def open_settings(self):
        self.main_frame.pack_forget()
        self.update_setting()
        self.settings_frame.pack(fill="both", expand=True)
        self.disable_move_player()

    def close_settings(self):
        self.settings_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def initialize_seed(self):
        """Initialize the seed for maze generation and rules."""
        if self.seed_input:
            try:
                self.maze_seed = int(self.seed_input)
            except ValueError:
                print("Invalid seed, generating a random one.")
                self.maze_seed = random.randint(1, 10**6)
        else:
            self.maze_seed = random.randint(1, 10**6)
        print(f"Using seed: {self.maze_seed}")
        random.seed(self.maze_seed)

    def initialize_rules(self):
        """Generate rules based on the current seed."""
        self.current_level = 1
        self.max_level = int(self.fsreach(self.configfile_path, "max_rules_count"))
        seed(self.maze_seed)  # Use the same seed as the maze

        rule_indices = list(ALL_RULES.keys())
        shuffle(rule_indices)  # Shuffle the rules based on the seed
        self.rules = {i + 1: ALL_RULES[rule_idx] for i, rule_idx in enumerate(rule_indices[:self.max_level])}
        self.rule_status = {i: False for i in range(1, self.max_level + 1)}
        self.rule_labels = {}

    def create_rule_label(self, level):
        """Tạo label mới cho rule"""
        rule_text = self.rules[level][0]
        label = ctk.CTkLabel(
            self.rules_frame,
            text=f"{level}. {rule_text}",
            font=("Comic Sans MS", 16, "bold"),
            text_color="red"
        )
        label.pack(pady=5, padx=10, anchor="w")
        self.rule_labels[level] = label

    def generate_maze(self):
        if self.maze_seed is not None:
            seed(self.maze_seed)

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

        self.images["wall"] = load_image("assets\level\wallStone_small.png")
        self.images["player"] = load_image("assets\hero\idleright\hero_idleB_0000.png")
        self.images["exit"] = load_image("assets\level\groundExit.png")
        self.images["path"] = load_image("assets\level\ground.png")

    def load_animation_frames(self, folder_path):
        """Load and resize animation frames from a given folder."""
        try:
            frames = []
            for file_name in sorted(os.listdir(folder_path)):
                if file_name.endswith(".png"):
                    image = Image.open(os.path.join(folder_path, file_name))
                    resized_image = image.resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
                    frames.append(ImageTk.PhotoImage(resized_image))
            return frames
        except:
            return -1

    def draw_maze(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x_center = x1 + self.cell_size // 2
                y_center = y1 + self.cell_size // 2

                if self.maze[row][col] == 1:
                    self.maze_canvas.create_image(x_center, y_center, image=self.images["wall"])
                else:
                    self.maze_canvas.create_image(x_center, y_center, image=self.images["path"])
        # Draw exit
        self.maze_canvas.create_image(
            self.exit_pos[1] * self.cell_size + self.cell_size // 2,
            self.exit_pos[0] * self.cell_size + self.cell_size // 2,
            image=self.images["exit"]
        )
        # Draw player
        self.player = self.maze_canvas.create_image(
            self.player_pos[1] * self.cell_size + self.cell_size // 2,
            self.player_pos[0] * self.cell_size + self.cell_size // 2,
            image=self.images["player"]
        )

    def update_fog(self):
        """Update the fog overlay to highlight only visited cells."""
        if self.fog_overlay:
            self.maze_canvas.delete(self.fog_overlay)

        # Create a fully black image
        fog_image = Image.new("RGBA", (self.grid_size * self.cell_size,
                                    self.grid_size * self.cell_size),
                                    (0, 0, 0, 255))
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
        for cell in self.visited_cells:
            px, py = cell
            x1 = py * self.cell_size
            y1 = px * self.cell_size
            for x in range(x1, x1 + self.cell_size):
                for y in range(y1, y1 + self.cell_size):
                    fog_image.putpixel((x, y), (0, 0, 0, 100))  # Set transparent pixels for visible area

        fog_tk = ImageTk.PhotoImage(fog_image)
        self.fog_overlay = self.maze_canvas.create_image(0, 0, image=fog_tk, anchor=tk.NW)
        self.maze_canvas.image = fog_tk  # Keep a reference to avoid garbage collection

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
            self.maze_canvas.itemconfig(self.player, image=frame)
            self.maze_canvas.coords(
                self.player,
                start_x + dx * (i + 1),
                start_y + dy * (i + 1)
            )
            self.root.update()
            
            self.root.after(int(self.fsreach(self.configfile_path, "animation_delay")))  # Delay between frames
    
    def allows_move_player(self, event = "none"):
        self.root.bind("<Up>", lambda event: self.move_player("up"))
        self.root.bind("<Down>", lambda event: self.move_player("down"))
        self.root.bind("<Left>", lambda event: self.move_player("left"))
        self.root.bind("<Right>", lambda event: self.move_player("right"))

    def disable_move_player(self):
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")

    def move_player(self, direction):
        self.check_password("")
        if self.is_moving or not self.is_allDone:
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

    def check_password(self, event):
        self.password = self.userinput.get()

        #Kiểm tra tất cả các quy tắc đã đúng hay chưa
        self.is_allDone = True
        self.need_help = True
        self.help_indicate = ""
        for level in range(1, self.current_level + 1):
            _, check_function = self.rules[level]
            is_valid = check_function(self.password)
            self.rule_status[level] = is_valid
            self.rule_labels[level].configure(
                text_color="white" if is_valid else "red"
            )
            if not is_valid:
                self.is_allDone = False
                if self.need_help:
                    self.help_indicate = self.rule_labels[level]
                    self.need_help = False

        if not self.is_allDone:
            return False
        else:
            return True
        #Kiểm tra chiến thắng hoặc mở level tiếp theo
        # if self.is_allDone:
        #     if self.current_level == self.max_level:
        #         if not hasattr(self, 'success_frame'):
        #             self.Success()
        #     else:
        #         self.current_level +=1
        #         self.create_rule_label(self.current_level)
        #         print(f"Hoàn thành tất cả đến level{self.current_level}")
        #         self.check_password(event)

    def on_enter_new_cell(self, cell):
        self.current_level +=1
        if self.current_level > self.max_level:
            self.win_game()
            return
        self.create_rule_label(self.current_level)
        self.check_password("")
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
            victory_frames = self.load_animation_frames("assets\hero\winA")
            for frame in victory_frames:
                self.maze_canvas.itemconfig(self.player, image=frame)
                self.root.update()
                self.root.after(100)


        self.is_Wingame = True
        
        self.disable_move_player() # Tắt khả năng di chuyển
        self.maze_canvas.delete(self.fog_overlay) #Xoá bóng đêm
        animate_victory() #Chạy hoạt ảnh chiến thắng
        
        replay_prompt() #mở bảng thông báo restart hay quit

    def reset_game(self):
        """Reset the game to start again."""
        self.is_Wingame = False
        self.player_pos = [0, 0]
        self.visited_cells = set()
        for label in self.rule_labels.values():
            label.destroy()
        self.visited_cells.add(tuple(self.player_pos))
        self.current_level =1
        self.initialize_seed()
        self.initialize_rules()
        self.maze = self.generate_maze()
        self.maze_canvas.delete("all")
        self.draw_maze()
        self.is_moving = False
        self.update_fog()
        self.allows_move_player()
        self.userinput.delete(0, 'end')
        self.create_rule_label(1)
        self.reset_event = True

    def update_timer(self):
        start_time = time.time()
        while self.running:
            if self.reset_event:  # Nếu reset, cập nhật lại thời gian bắt đầu
                start_time = time.time()
                self.elapsed_time = 0
                self.reset_event = False

            self.elapsed_time = time.time() - start_time
            hours, remainder = divmod(self.elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = int((self.elapsed_time - int(self.elapsed_time)) * 100)
            self.timer_label.configure(
                text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{milliseconds:02}"
            )
            time.sleep(0.01)
         
    def fsreach(self, file_path, keyword):
        # Đọc file và tìm giá trị sau dấu '=' của từ khoá
        # return value nếu tìm thấy giá trị, return -1 nếu tệp không tồn tại hoặc lỗi khác, return "" nếu không có tìm thấy từ khoá
        try:
            with open(file_path, 'r') as file:  # Mở tệp trong chế độ đọc
                for line in file:  # Duyệt qua từng dòng trong tệp
                    if keyword in line:  # Kiểm tra xem từ khóa có trong dòng không
                        # Tách giá trị sau dấu '=' và loại bỏ khoảng trắng
                        parts = line.split('=')  
                        if len(parts) > 1:
                            value = parts[1].strip()  # Lấy phần sau dấu '=' và loại bỏ khoảng trắng
                            return value
            return "" #f"Từ khóa '{keyword}' không tìm thấy trong tệp."
        except FileNotFoundError:
            return -1
        except Exception as e:
            return 0 #f"Lỗi: {e}"


if __name__ == "__main__":
    root = ctk.CTk()
    game = MazeGame(root)
    root.mainloop()
