import tkinter as tk

# Hàm để cuộn Canvas khi cuộn chuột
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Cuộn qua nhiều Label với chuột")

# Tạo một Canvas
canvas = tk.Canvas(root)
canvas.grid(row=0, column=0, sticky="nsew")

# Tạo một Frame trong Canvas để chứa các Label
frame = tk.Frame(canvas)

# Đặt Frame vào Canvas
canvas.create_window((0, 0), window=frame, anchor="nw")

# Thêm các Label vào Frame
for i in range(30):  # Thêm 30 Label cho ví dụ
    label = tk.Label(frame, text=f"Label {i+1}")
    label.grid(row=i, column=0, pady=5)

# Cập nhật vùng hiển thị của Canvas sau khi thêm các Label
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Liên kết sự kiện cuộn chuột với Canvas
canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows và MacOS sử dụng <MouseWheel>

# Thiết lập cấu hình kích thước cửa sổ
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Chạy ứng dụng
root.mainloop()
