import customtkinter as ctk
import time
from threading import Thread

# Hàm đếm thời gian
def update_timer():
    global elapsed_time, reset_event
    start_time = time.time()
    while running:
        if reset_event:  # Nếu reset, cập nhật lại thời gian bắt đầu
            start_time = time.time()
            elapsed_time = 0
            reset_event = False

        elapsed_time = time.time() - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((elapsed_time - int(elapsed_time)) * 100)
        timer_label.configure(
            text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{milliseconds:02}"
        )
        time.sleep(0.01)

# Hàm reset thời gian
def reset_timer():
    global reset_event
    reset_event = True

# Khởi tạo giao diện
app = ctk.CTk()
app.geometry("400x250")
app.title("Đồng hồ đếm thời gian")

# Label hiển thị thời gian
timer_label = ctk.CTkLabel(app, text="00:00:00:00", font=("Arial", 24))
timer_label.pack(pady=20)

# Nút Reset
reset_button = ctk.CTkButton(app, text="Reset", command=reset_timer, font=("Arial", 14))
reset_button.pack(pady=10)

# Chạy đồng hồ trong luồng riêng
running = True
reset_event = False
elapsed_time = 0
thread = Thread(target=update_timer, daemon=True)
thread.start()

# Sự kiện đóng ứng dụng
def on_closing():
    global running
    running = False
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

# Chạy ứng dụng
app.mainloop()
