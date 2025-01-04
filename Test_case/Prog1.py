import customtkinter as ctk
import re
from tkinter import messagebox

class PasswordGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Cấu hình cửa sổ
        self.title("Password Game")
        self.geometry("600x500")
        
        # Khởi tạo biến
        self.current_level = 1
        self.max_level = 5
        
        # Khởi tạo rules trước khi setup UI
        self.rules = {
            1: ("Mật khẩu phải có ít nhất 5 ký tự", self.check_length),
            2: ("Phải có ít nhất 1 chữ hoa", self.check_uppercase),
            3: ("Phải có ít nhất 1 số", self.check_number),
            4: ("Phải có ít nhất 1 ký tự đặc biệt (!@#$%^&*)", self.check_special),
            5: ("Tổng các số trong mật khẩu phải là 10", self.check_sum_10)
        }
        
        # Sau đó mới setup UI
        self.setup_ui()

    def setup_ui(self):
        # Label hướng dẫn
        self.label_title = ctk.CTkLabel(
            self,
            text="Hãy tạo mật khẩu theo yêu cầu!",
            font=("Arial", 20, "bold")
        )
        self.label_title.pack(pady=20)

        # Label hiển thị rule hiện tại
        self.label_rule = ctk.CTkLabel(
            self,
            text=self.rules[1][0],
            font=("Arial", 16)
        )
        self.label_rule.pack(pady=10)

        # Entry để nhập mật khẩu
        self.password_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Nhập mật khẩu của bạn"
        )
        self.password_entry.pack(pady=20)

        # Nút kiểm tra
        self.check_button = ctk.CTkButton(
            self,
            text="Kiểm tra",
            command=self.check_password
        )
        self.check_button.pack(pady=10)

        # Label hiển thị level
        self.label_level = ctk.CTkLabel(
            self,
            text=f"Level: {self.current_level}/{self.max_level}",
            font=("Arial", 14)
        )
        self.label_level.pack(pady=10)

    def check_length(self, password):
        return len(password) >= 5

    def check_uppercase(self, password):
        return any(c.isupper() for c in password)

    def check_number(self, password):
        return any(c.isdigit() for c in password)

    def check_special(self, password):
        return any(c in "!@#$%^&*" for c in password)

    def check_sum_10(self, password):
        numbers = [int(c) for c in password if c.isdigit()]
        return sum(numbers) == 10 if numbers else False

    def check_password(self):
        password = self.password_entry.get()
        rule_text, check_function = self.rules[self.current_level]
        
        if check_function(password):
            if self.current_level == self.max_level:
                messagebox.showinfo("Chúc mừng!", "Bạn đã chiến thắng trò chơi!")
                self.quit()
            else:
                self.current_level += 1
                self.label_rule.configure(text=self.rules[self.current_level][0])
                self.label_level.configure(text=f"Level: {self.current_level}/{self.max_level}")
                messagebox.showinfo("Tốt lắm!", "Hãy tiếp tục với quy tắc tiếp theo!")
        else:
            messagebox.showerror("Lỗi", "Mật khẩu chưa đáp ứng yêu cầu hiện tại!")

if __name__ == "__main__":
    app = PasswordGame()
    app.mainloop()