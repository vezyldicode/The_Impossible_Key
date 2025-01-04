import customtkinter as ctk
import re
from tkinter import messagebox
import random

class PasswordGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Cấu hình cửa sổ
        self.title("Password Game")
        self.geometry("600x700")
        
        # Khởi tạo biến
        self.current_level = 1
        self.max_level = 5
        
        # Khởi tạo tất cả các rules có thể có
        self.all_rules = {
            1: ("Mật khẩu phải có ít nhất 5 ký tự", self.check_length),
            2: ("Phải có ít nhất 1 chữ hoa", self.check_uppercase),
            3: ("Phải có ít nhất 1 số", self.check_number),
            4: ("Phải có ít nhất 1 ký tự đặc biệt (!@#$%^&*)", self.check_special),
            5: ("Tổng các số trong mật khẩu phải là 10", self.check_sum_10),
            6: ("Phải có ít nhất 3 chữ cái", self.check_three_letters),
            7: ("Phải chứa từ 'password'", self.check_contains_password),
            8: ("Phải có số chẵn", self.check_even_number),
            9: ("Phải có ít nhất 2 ký tự đặc biệt", self.check_two_special),
            10: ("Độ dài phải là số lẻ", self.check_odd_length)
        }
        
        # Chọn ngẫu nhiên 5 rules
        rule_indices = random.sample(list(self.all_rules.keys()), self.max_level)
        self.rules = {i+1: self.all_rules[rule_idx] for i, rule_idx in enumerate(rule_indices)}
        
        # Dictionary để lưu trạng thái của các rules
        self.rule_status = {i: False for i in range(1, self.max_level + 1)}
        
        # Dictionary để lưu các rule labels
        self.rule_labels = {}
        
        self.setup_ui()

    def setup_ui(self):
        # Label hướng dẫn
        self.label_title = ctk.CTkLabel(
            self,
            text="Hãy tạo mật khẩu theo yêu cầu!",
            font=("Cascadia Mono", 20, "bold")
        )
        self.label_title.pack(pady=20)

        # Label hiển thị rule hiện tại
        self.label_current_rule = ctk.CTkLabel(
            self,
            text="Quy tắc hiện tại:",
            font=("Arial", 16, "bold")
        )
        self.label_current_rule.pack(pady=5)

        self.label_rule = ctk.CTkLabel(
            self,
            text=self.rules[1][0],
            font=("Arial", 16)
        )
        self.label_rule.pack(pady=5)

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

        # Frame chứa các rule status
        self.rules_frame = ctk.CTkFrame(self)
        self.rules_frame.pack(pady=20, padx=20, fill="x")

        # Label tiêu đề cho phần trạng thái
        self.label_status_title = ctk.CTkLabel(
            self.rules_frame,
            text="Các quy tắc đã mở khóa:",
            font=("Arial", 16, "bold")
        )
        self.label_status_title.pack(pady=10)

        # Tạo label cho rule đầu tiên
        self.create_rule_label(1)

        # Bind sự kiện khi người dùng nhập
        self.password_entry.bind('<KeyRelease>', self.on_password_change)

    def create_rule_label(self, level):
        """Tạo label mới cho rule"""
        rule_text = self.rules[level][0]
        label = ctk.CTkLabel(
            self.rules_frame,
            text=f"{level}. {rule_text}",
            font=("Arial", 14),
            text_color="red"
        )
        label.pack(pady=5, padx=10, anchor="w")
        self.rule_labels[level] = label

    def on_password_change(self, event):
        password = self.password_entry.get()
        for level in range(1, self.current_level + 1):
            _, check_function = self.rules[level]
            is_valid = check_function(password)
            self.rule_status[level] = is_valid
            self.rule_labels[level].configure(
                text_color="white" if is_valid else "red"
            )

    # Các hàm kiểm tra cũ
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

    # Các hàm kiểm tra mới
    def check_three_letters(self, password):
        return sum(1 for c in password if c.isalpha()) >= 3

    def check_contains_password(self, password):
        return 'password' in password.lower()

    def check_even_number(self, password):
        numbers = [int(c) for c in password if c.isdigit()]
        return any(n % 2 == 0 for n in numbers)

    def check_two_special(self, password):
        return sum(1 for c in password if c in "!@#$%^&*") >= 2

    def check_odd_length(self, password):
        return len(password) % 2 == 1

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
                self.create_rule_label(self.current_level)
                messagebox.showinfo("Tốt lắm!", "Hãy tiếp tục với quy tắc tiếp theo!")
        else:
            messagebox.showerror("Lỗi", "Mật khẩu chưa đáp ứng yêu cầu hiện tại!")

if __name__ == "__main__":
    app = PasswordGame()
    app.mainloop()