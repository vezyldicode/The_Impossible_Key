import tkinter as tk

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Cuộn qua nhiều Label")

# Tạo một Canvas và một Scrollbar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

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

# Đặt Canvas và Scrollbar lên giao diện
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Thiết lập cấu hình kích thước cửa sổ
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Chạy ứng dụng
root.mainloop()
