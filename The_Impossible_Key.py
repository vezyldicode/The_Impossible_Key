import customtkinter as Ctk
import re
from tkinter import font
import random
from PIL import Image, ImageTk
import os
from assets.quizzes.Rules_Dictionary import *

class Metadata:
    App_name = "Who nees a password like this"
    current_dir = os.getcwd()
    

class The_Impossible_Key(Ctk.CTk):
    class attribute:
        width = 800
        height = 800
        bg = '#2A3335'
        textcolor = '#FFF0DC'
        wrongcolor = '#D91656'
        helpImage = os.path.join(Metadata.current_dir, 'Image', 'helpbtn.png')

    def theme_change(self):
        if self.theme == "dark":
            Ctk.set_appearance_mode("light")
            self.theme = "light"


            self.update_idletasks()
        else:
            Ctk.set_appearance_mode("dark")
            self.theme = "dark"
            self.update_idletasks()


    def level_change(self, event=None):
        self.levelUI.configure(text=self.modeslider.get())

    def __init__(self):
        super().__init__() #Gọi init của Ctk
        #UI_var
        self.theme='dark' #default = dark
        self.width = 800
        self.height = 800
        self.bg = '#2A3335'
        self.textcolor = '#FFF0DC'
        self.wrongcolor = '#D91656'
        helpImage = os.path.join(Metadata.current_dir, 'Image', 'helpbtn.png')

        #Window Config
        self.title(Metadata.App_name)
        self.geometry(f"{self.width}x{self.height}")

        #Khởi tạo biến ban đầu
        self.max_level = 3
        self.current_level = 1
        
        self.initialize_game()
        self.setup_ui()

    def setup_ui(self):
        #======================nav_bar======================
        self.nav_bar = Ctk.CTkFrame(
            self,
            height=35)
        self.nav_bar.pack(padx =5, pady =5, fill='x')
        #nav_bar widgets
        
        #Đổi theme
        self.theme_switch = Ctk.CTkSwitch(
            self.nav_bar,
            text='theme',
            font=('Comic Sans MS', 15),
            corner_radius=32,
            command=self.theme_change
        )
        self.theme_switch.pack(side="left", padx=10, pady=10)

        #Tạo game mới
        self.Restartbtn = Ctk.CTkButton(
            self.nav_bar,
            text = "New Game",
            font=('Comic Sans MS', 15),
            corner_radius=32,
            command=self.restart_game
        )
        self.Restartbtn.pack(side="left", padx=10, pady=10)

        #Độ khó
        self.modeslider = Ctk.CTkSlider(
            self.nav_bar,
            from_=0,
            to=40,
            number_of_steps=40,
            command=self.level_change
        )
        self.modeslider.pack(side="left", padx=10, pady=10)

        self.levelUI = Ctk.CTkLabel(
            self.nav_bar,
            text="20",
            font=('Comic Sans MS', 15),
        )
        self.levelUI.pack(side="left", padx=10, pady=10)

        #Nút trợ giúp
        self.helpbtn = Ctk.CTkButton(
            self.nav_bar,
            text = "",
            font=('Comic Sans MS', 15),
            corner_radius=32,
            command=self.help,
            width = 30
        )
        self.helpbtn.pack(side="right", padx=10, pady=10)

        #======================nav_bar======================

        #Title
        self.label_title = Ctk.CTkLabel(
            self,
            text="Write down your password",
            font=('Cascadia Code SemiBold', 25), 
            text_color=self.textcolor if self.theme == 'dark' else self.bg,
        )
        self.label_title.pack(padx=20, pady=20, anchor="center")

        #Vùng nhập mật khẩu
        self.userinput = Ctk.CTkEntry(
            self,
            placeholder_text="Write Here",
            font=('Cascadia Mono', 18),
            fg_color='#F4F4F4',
            text_color='black',
            height=40,
            corner_radius=10
        )
        self.userinput.pack(padx=90, pady=20, anchor="center", fill="x")
        self.userinput.bind("<KeyRelease>", self.password_change)

        #Frame chứa các rule status
        self.rules_frame = Ctk.CTkScrollableFrame(self)
        self.rules_frame.pack(padx=90, pady=20, fill="both", expand=True)

        #Tittle của Frame
        self.label_status_title = Ctk.CTkLabel(
            self.rules_frame,
            text="Rules",
            font=("Comic Sans MS", 20, "bold")
        )
        self.label_status_title.pack(pady=10)
        self.create_rule_label(1)
        
    
    def create_rule_label(self, level):
        """Tạo label mới cho rule"""
        rule_text = self.rules[level][0]
        label = Ctk.CTkLabel(
            self.rules_frame,
            text=f"{level}. {rule_text}",
            font=("Comic Sans MS", 16, "bold"),
            text_color="red"
        )
        label.pack(pady=5, padx=10, anchor="w")
        self.rule_labels[level] = label

    def initialize_game(self):
        """Khởi tạo/Khởi động lại các biến của trò chơi"""
        self.current_level = 1
        rule_indices = random.sample(list(ALL_RULES.keys()), self.max_level)
        self.rules = {i+1: ALL_RULES[rule_idx] for i, rule_idx in enumerate(rule_indices)}
        self.rule_status = {i: False for i in range(1, self.max_level + 1)}
        self.rule_labels = {}

    def password_change(self, event):
        print("Dang kiem tra...")
        self.password = self.userinput.get()
        print (self.password)

        #Kiểm tra tất cả các quy tắc đã đúng hay chưa
        self.is_allDone = True
        self.need_help = True
        self.help_indicate = ""
        for level in range(1, self.current_level + 1):
            _, check_function = self.rules[level]
            is_valid = check_function(self.password)
            self.rule_status[level] = is_valid
            self.rule_labels[level].configure(
                text_color="white" if is_valid else "red"
            )
            if not is_valid:
                self.is_allDone = False
                if self.need_help:
                    self.help_indicate = self.rule_labels[level]
                    self.need_help = False

        #Kiểm tra chiến thắng hoặc mở level tiếp theo
        if self.is_allDone:
            if self.current_level == self.max_level:
                if not hasattr(self, 'success_frame'):
                    self.Success()
            else:
                self.current_level +=1
                self.create_rule_label(self.current_level)
                print(f"Hoàn thành tất cả đến level{self.current_level}")
                self.password_change(event)
            
    def help(self):
        # self.password_change
        # try:
        #     self.help_indicate.configure(
        #         text_color="black"
        #     )
        # except:
        #     print("cút")
        pass

    def Success(self):
        print("Bạn đã chiến thắng")
        self.success_frame = Ctk.CTkFrame(self, 
                                        width=500,
                                        height=200,
                                        corner_radius=15,)
        self.success_frame.place(relx=0.5,
                                 rely=0.5,
                                 anchor="center"
                                 )
        print("Đang gọi . Frame hiện tại:", self.success_frame)

        title = Ctk.CTkLabel(self.success_frame,
                              text="Bạn đã chiến thắng")
        title.pack(pady=(20, 10))  # Thêm khoảng cách trên và dưới

        # Label dòng 2: "Bạn muốn chơi lại không?"
        question = Ctk.CTkLabel(self.success_frame,
                              text="Bạn muốn chơi lại không?")
        question.pack(pady=(0, 20))

        # Nút "Chơi lại"
        replay_button = Ctk.CTkButton(self.success_frame,
                                      text="Chơi lại",
                                      command=self.Replay)
        replay_button.pack(side="left", padx=(40, 10), pady=10)

        # Nút "Xem review"
        review_button = Ctk.CTkButton(self.success_frame,
                                      text="Xem review",
                                      command=self.review)
        review_button.pack(side="right", padx=(10, 40), pady=10)

    def review(self):
            print("Đang gọi review. Frame hiện tại:", self.success_frame)
            self.success_frame.destroy()
            self.update_idletasks()
    def Replay(self):
            self.success_frame.destroy()
            self.restart_game()

    def restart_game(self):
        """Khởi động lại trò chơi"""   
        # Xóa nội dung password entry
        self.userinput.delete(0, 'end')
        
        # Xóa tất cả rule labels cũ
        for label in self.rule_labels.values():
            label.destroy()  # Xóa widget nếu tồn tại phương thức destroy

        # Reset trò chơi
        self.initialize_game()
        # Tạo label cho rule đầu tiên
        self.create_rule_label(1)
        
    
def main():
    app = The_Impossible_Key()
    app.mainloop()

if __name__ == '__main__':
    main()

