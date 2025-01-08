import customtkinter as ctk

# Khởi tạo giao diện
app = ctk.CTk()
app.geometry("400x300")

# Tạo Frame chứa label
frame = ctk.CTkFrame(app)
frame.pack(fill="both", expand=True, padx=20, pady=20)

# Tạo Label
label = ctk.CTkLabel(
    frame,
    text="Đây là một đoạn văn bản dài. Văn bản này sẽ tự động căn chỉnh để phù hợp với chiều rộng của frame khi cửa sổ thay đổi kích thước.",
    font=("Arial", 14),
    justify="left"  # Căn lề trái, có thể dùng 'center' hoặc 'right' nếu cần
)
label.pack(fill="both", expand=True, padx=10, pady=10)

# Hàm cập nhật wraplength khi thay đổi kích thước cửa sổ
def update_wraplength(event):
    label.configure(wraplength=frame.winfo_width()-20)  # Trừ padding

# Liên kết sự kiện thay đổi kích thước
app.bind("<Configure>", update_wraplength)

# Hiển thị giao diện
app.mainloop()
