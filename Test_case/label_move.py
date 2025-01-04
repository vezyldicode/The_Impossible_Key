import tkinter as tk

# Hàm để di chuyển label lên row 0
def move_label():
    # Lấy row hiện tại của label
    current_row = label.grid_info()["row"]
    
    # Di chuyển label lên row 0 (nếu label chưa ở row 0)
    if int(current_row) > 0:
        # Cập nhật row mới cho label
        label.grid(row=int(current_row) - 1, column=0)
        
        # Gọi lại hàm này sau 20ms (0.02s) để tiếp tục di chuyển
        root.after(2000, move_label)

# Tạo cửa sổ Tkinter
root = tk.Tk()
root.title("Hiệu ứng Di chuyển Label lên row 0")

# Kích thước cửa sổ
root.geometry("500x300")

# Tạo label ở row 2
label = tk.Label(root, text="Di chuyển tôi lên row 0!", font=("Arial", 14))
label.grid(row=2, column=0, padx=20, pady=20)

# Bắt đầu di chuyển label
move_label()

# Chạy ứng dụng Tkinter
root.mainloop()
