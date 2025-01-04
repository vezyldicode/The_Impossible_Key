import tkinter as tk

root = tk.Tk()

# Tạo một Frame đại diện cho row=0, column=1 với viền
frame_with_border = tk.Frame(root, bd=2, relief="solid")
frame_with_border.grid(row=0, column=1, padx=10, pady=10)  # Đặt Frame vào grid

# Thêm Label vào Frame
label_inside = tk.Label(frame_with_border, text="Hello, Grid!", bg="lightblue", fg="black")
label_inside.pack(padx=10, pady=10)  # Đặt Label bên trong Frame

# Thêm một Label khác ở một ô khác để minh họa layout
other_label = tk.Label(frame_with_border, text="Another cell", bg="lightgreen")
other_label.pack()
# other_label.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()
