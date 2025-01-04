import customtkinter as ctk
import time

def fade_in_label(label, step=0.05, interval=10):
    """Hàm tạo hiệu ứng mờ dần cho CTkLabel."""
    for alpha in range(0, 101, int(step * 100)):  # Alpha từ 0 đến 100
        color = f"#{int(255 * (1 - alpha / 100)):02x}{int(255 * (1 - alpha / 100)):02x}{int(255 * (1 - alpha / 100)):02x}"
        label.configure(fg_color=color)
        label.update()
        time.sleep(interval / 1000)  # Chuyển ms thành giây

# Khởi tạo giao diện customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Tạo cửa sổ
app = ctk.CTk()
app.geometry("400x300")
app.title("Fade In Label")

# Tạo label
label = ctk.CTkLabel(app, text="Hello, this is a fade-in effect for a label!", 
                     font=("Arial", 16), fg_color="black")
label.place(relx=0.5, rely=0.5, anchor="center")

# Bắt đầu hiệu ứng fade in cho label
fade_in_label(label)

# Chạy ứng dụng
app.mainloop()
