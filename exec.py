from lib import file_handler as file
from lib.Rules import *
import tkinter as tk
from tkinter import *
from tkinter import font
import random
from PIL import Image, ImageTk
import os

class Metadata:
    name = "Who nees a password like this"
    current_dir = os.getcwd()
    

class Program_attribute:
    Password = ""
    First_rule = True
    isAllDone = True
    Rule_object = []
    Label_object = []
    Wrong_cond_order = 0
    Correct_cond_order = 0
    Max_rules_count = 12
    Finish_game_total = 10

class filePath:
    testcase = 'Test_case\\casetest1.txt'


class UIattribute :
    name = "Who nees a password like this"
    Width = 800
    Height = 800
    bg = '#2A3335'
    textcolor = '#FFF0DC'
    wrongcolor = '#D91656'
    helpImage = os.path.join(Metadata.current_dir, 'Image', 'helpbtn.png')


def Random_rule():
    while True:
        number = random.randint(2, Program_attribute.Max_rules_count)
        
        # Kiểm tra nếu rule đã tồn tại trong Rule_object
        if f"Rule{number}" not in Program_attribute.Rule_object:
            print(f"Tạo rule{number}")
            Program_attribute.Rule_object.append(f"Rule{number}")
            break  # Dừng vòng lặp khi tạo thành công

def Label_rearrange(index):
    Program_attribute.Label_object[index].config(fg = 'red')


def Rules_check():
    i =0
    for element in (Program_attribute.Rule_object):
        result = globals()[element](0, 0, 0, Program_attribute.Password)
        if result == -1:
            Program_attribute.isAllDone = False
            Program_attribute.Label_object[i].config(fg = UIattribute.wrongcolor, bg=UIattribute.bg)
            Program_attribute.Label_object[i].grid(row=Program_attribute.Wrong_cond_order, column=0, pady=5, sticky="w")
            Program_attribute.Wrong_cond_order +=1
            Program_attribute.Correct_cond_order = Program_attribute.Wrong_cond_order +1
        i+=1
    i=0
    for element in (Program_attribute.Rule_object):
        result = globals()[element](0, 0, 0, Program_attribute.Password)
        if result == 0:
            Program_attribute.Label_object[i].config(fg = UIattribute.textcolor, bg=UIattribute.bg)
            Program_attribute.Label_object[i].grid(row=Program_attribute.Correct_cond_order, column=0, pady=5, sticky="w")
            Program_attribute.Correct_cond_order +=1
        i +=1

# cửa sổ chính
def Contructor():
    console = tk.Tk()
    basefont = font.Font(family="Comic Sans MS", size=14)
    console.resizable(False, False)
    console.config(bg=UIattribute.bg)

    console.geometry(f"{UIattribute.Width}x{UIattribute.Height}")
    console.title(UIattribute.name)
    
    img = Image.open(UIattribute.helpImage)
    img_resized = img.resize((25, 25))
    photo = ImageTk.PhotoImage(img_resized)
    help_btn = tk.Button(console, image=photo, bg=UIattribute.bg)
    help_btn.place(x = UIattribute.Width - 50, y=10, width=30, height=30)


    label =tk.Label(console, text="Write down your password", font=('Cascadia Code SemiBold', 16),fg=UIattribute.textcolor, bg=UIattribute.bg)
    label.pack(padx=20, pady=20)


    userInput = tk.Text(console, height=3, font=('Cascadia Mono', 14), bg='#F4F4F4')
    userInput.bind("<KeyRelease>", lambda event, Input=userInput: password_change(event, Input))
    userInput.pack(padx=20, pady=5)

    canvas = tk.Canvas(console, bg=UIattribute.bg)
    canvas.pack(padx=20, side="left", fill="both", expand=True)

    frame = tk.Frame(canvas, bg=UIattribute.bg)

    console.grid_rowconfigure(0, weight=1)
    console.grid_columnconfigure(0, weight=1)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    # for i in range(30):  # Thêm 30 Label cho ví dụ
    #     label = tk.Label(frame, text=f"Label {i+1}")
    #     label.grid(row=i, column=0, pady=5)
    
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        
    def password_change(event, Input):
        # đưa ra rule mặc định đầu tiên
        Program_attribute.Password = userInput.get("1.0", "end-1c")
        if Program_attribute.First_rule == True:
            Program_attribute.Rule_object.append(f"Rule1")
            label = globals()[Program_attribute.Rule_object[0]](1, frame, basefont, Program_attribute.Password)
            label.grid(row=Program_attribute.Correct_cond_order, column=0, pady=5, sticky="w")
            Program_attribute.Correct_cond_order +=1
            Program_attribute.Label_object.append(label)
            
            Program_attribute.First_rule = False

        # Kiểm tra tính đúng của tất cả các rule
        Program_attribute.isAllDone = True
        Rules_check()

        # nếu tất cả rule hiện có đúng thì hiển thị rule mới
        if Program_attribute.isAllDone == True:
            if len(Program_attribute.Rule_object) == Program_attribute.Finish_game_total:
                print("Thanh Cong")
                return
            
            # Khởi tạo 1 rule ngẫu nhiên
            Random_rule()

            # Hiển thị rule đó lên màn hình
            new_rule = globals()[Program_attribute.Rule_object[-1]](1, frame, basefont, Program_attribute.Password)
            new_rule.grid(row=Program_attribute.Correct_cond_order, column=0, pady=5, sticky="w")
            Program_attribute.Correct_cond_order +=1

            # Lưu label vào Label list
            Program_attribute.Label_object.append(new_rule)
            
            #Xét các trường hợp dynamic rule
            match Program_attribute.Rule_object[-1]:
                case "Rule5":
                    captcha_label = Program_attribute.Label_object[-1]
                    new_rule.bind("<Button-1>", re_captcha)


            #Gọi lại hàm password change để kiểm tra mật khẩu đã chính xác với rule mới tạo chưa
            password_change(0, Program_attribute.Password)

        console.update_idletasks()
        Rules_check()

    console.mainloop()



if __name__ == '__main__':
    Contructor()

