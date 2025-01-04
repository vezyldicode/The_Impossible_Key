import tkinter as tk
from tkinter import *
from tkinter import font

class UIattribute :
    name = "Who nees a password like this"
    Width = 700
    Height = 800
    def __init__(self, width = 500, height = 400):
        self.width = width
        self.height = height


# cửa sổ chính
def Contructor():
    console = tk.Tk()
    basefont = font.Font(family="Helvetica", size=16)
    console.resizable(False, False)

    console.geometry(f"{UIattribute.Width}x{UIattribute.Height}")
    console.title(UIattribute.name)
    
    help_btn = tk.Button(console, text ="🆘")
    help_btn.place(x = UIattribute.Width - 50, y=10, width=30, height=30)
    label =tk.Label(console, text="Write down your password", font=basefont)
    label.pack(padx=20, pady=20)


    userInput = tk.Text(console, height=3, font=basefont)
    userInput.bind("<KeyRelease>", lambda event, password=userInput: password_change(event, password))
    userInput.pack(padx=20, pady=5)

    canvas = tk.Canvas(console)
    canvas.pack(side="left", fill="both", expand=True)

    frame = tk.Frame(canvas)

    console.grid_rowconfigure(0, weight=1)
    console.grid_columnconfigure(0, weight=1)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    for i in range(30):  # Thêm 30 Label cho ví dụ
        label = tk.Label(frame, text=f"Label {i+1}")
        label.grid(row=i, column=0, pady=5)
    create_label(console, basefont)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    console.mainloop()
     
def password_change(event, password):
    print(password.get("1.0", "end-1c"))



if __name__ == '__main__':
    Contructor()
