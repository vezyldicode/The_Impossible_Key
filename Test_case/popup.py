import customtkinter as ctk

def replay():
    print("Chơi lại!")
    popup_frame.destroy()  # Đóng popup

def review():
    print("Xem review!")
    popup_frame.destroy()  # Đóng popup

# Khởi tạo ứng dụng
app = ctk.CTk()
app.geometry("500x400")

# Tạo Frame Popup
popup_frame = ctk.CTkFrame(app, width=300, height=200, corner_radius=15)
popup_frame.place(relx=0.5, rely=0.5, anchor="center")  # Đặt chính giữa cửa sổ

# Label dòng 1: "Bạn đã chiến thắng"
label1 = ctk.CTkLabel(popup_frame, text="Bạn đã chiến thắng", font=ctk.CTkFont(size=18, weight="bold"))
label1.pack(pady=(20, 10))  # Thêm khoảng cách trên và dưới

# Label dòng 2: "Bạn muốn chơi lại không?"
label2 = ctk.CTkLabel(popup_frame, text="Bạn muốn chơi lại không?", font=ctk.CTkFont(size=14))
label2.pack(pady=(0, 20))

# Nút "Chơi lại"
replay_button = ctk.CTkButton(popup_frame, text="Chơi lại", command=replay)
replay_button.pack(side="left", padx=(40, 10), pady=10)

# Nút "Xem review"
review_button = ctk.CTkButton(popup_frame, text="Xem review", command=review)
review_button.pack(side="right", padx=(10, 40), pady=10)

app.mainloop()
