import customtkinter as ctk

# Khởi tạo giao diện CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Tạo cửa sổ chính
root = ctk.CTk()
root.title("Copy Text to Clipboard")
root.geometry("400x200")

# Tạo Label 1 và gắn sự kiện
label1 = ctk.CTkLabel(root, text="Label 1: Sao chép tôi", font=("Arial", 16))
label1.pack(pady=10)
label1.bind("<Button-1>", lambda event: (root.clipboard_clear(), root.clipboard_append(event.widget.cget("text"))))

# Tạo Label 2 và gắn sự kiện
label2 = ctk.CTkLabel(root, text="Label 2: Nhấn để sao chép", font=("Arial", 16))
label2.pack(pady=10)
label2.bind("<Button-1>", lambda event: (root.clipboard_clear(), root.clipboard_append(event.widget.cget("text"))))

# Chạy ứng dụng
root.mainloop()
