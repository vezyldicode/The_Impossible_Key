import customtkinter as ctk

root = ctk.CTk()  # Tạo cửa sổ chính

# Label 1
label1 = ctk.CTkLabel(root, text="Label 1")
label1.pack(padx=10)

# Label 2
label2 = ctk.CTkLabel(root, text="Label 2")
label2.pack(side="left", padx=10,expand = True, fill = "both")

# Label 3 bên dưới Label 1
label3 = ctk.CTkLabel(root, text="Label 3")
label3.pack(padx=10, pady=10)  # Hiển thị bên dưới Label 1

root.mainloop()
