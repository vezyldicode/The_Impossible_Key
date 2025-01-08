import customtkinter as ctk

# Initialize the application window
app = ctk.CTk()
app.title("CustomTkinter Example")
app.geometry("400x300")

# Global variables to store seed and level values
seed_value = 0
level_value = 0

def show_setting_tab():
    """Switch to the settings tab."""
    for widget in app.winfo_children():
        widget.pack_forget()
    setting_tab.pack(fill="both", expand=True)

def save_settings():
    """Save the settings and return to the main tab."""
    global seed_value, level_value
    try:
        seed_value = int(seed_entry.get())
        level_value = int(level_entry.get())
        output_label.configure(text=f"Seed: {seed_value}, Level: {level_value}")
        show_main_tab()
    except ValueError:
        output_label.configure(text="Invalid input! Please enter integers.")

def show_main_tab():
    """Switch to the main tab."""
    for widget in app.winfo_children():
        widget.pack_forget()
    output_label.pack(pady=20)
    setting_button.pack()

# Main tab layout
output_label = ctk.CTkLabel(app, text="Seed: 0, Level: 0", font=("Arial", 14))
output_label.pack(pady=20)

setting_button = ctk.CTkButton(app, text="Settings", command=show_setting_tab)
setting_button.pack()

# Settings tab layout
setting_tab = ctk.CTkFrame(app)

seed_label = ctk.CTkLabel(setting_tab, text="Seed:")
seed_label.pack(pady=5)

seed_entry = ctk.CTkEntry(setting_tab)
seed_entry.pack(pady=5)

level_label = ctk.CTkLabel(setting_tab, text="Level:")
level_label.pack(pady=5)

level_entry = ctk.CTkEntry(setting_tab)
level_entry.pack(pady=5)

save_button = ctk.CTkButton(setting_tab, text="Save", command=save_settings)
save_button.pack(pady=20)

back_button = ctk.CTkButton(setting_tab, text="Back", command=show_main_tab)
back_button.pack()

# Start with the main tab
show_main_tab()

# Run the application
app.mainloop()
