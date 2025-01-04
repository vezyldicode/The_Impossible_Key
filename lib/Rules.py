import tkinter as tk
from captcha.image import ImageCaptcha
from PIL import Image, ImageTk
from io import BytesIO
import random
import string
import re
"""
Trong 1 hàm Rule sẽ bao gồm:
    1. hiển thị chữ
    2. kiểm tra điều kiện trong text với password
    3. nếu điều kiện đúng thì trả về 0, nếu sai trả về -1
    4. 
"""

class OTP:
    captcha_text = 0


def generate_random_string():
    # Ký tự hợp lệ: chữ cái in hoa, chữ cái in thường, và chữ số
    valid_characters = string.ascii_letters + string.digits
    # Tạo chuỗi ngẫu nhiên gồm 6 ký tự
    random_string = ''.join(random.choices(valid_characters, k=6))
    return random_string


def Rule1(action, parent, font, password):
    # Hiển thị chữ thông báo yêu cầu
    if action ==1:
        label = tk.Label(parent, text="Password phải có ít nhất 8 kí tự", font=font, anchor="w", fg = 'red')
        return label
    else:
        # Kiểm tra điều kiện trong text với password
        if len(password) >= 8:
            
            return 0  # Nếu điều kiện đúng, trả về 0
        else:
            return -1  # Nếu điều kiện sai, trả về -1


def Rule2(action, parent, font, password):
    if action ==1:
        label = tk.Label(parent, text="Ký tự đầu tiên phải trùng với ký tự cuối cùng của mật khẩu.", font=font, anchor="w", fg = 'red')
        return label
    else:
        if len(password) > 0:
            if password[0] == password[-1]:
                return 0
        return -1


def Rule3(action, parent, font, password):
    fibs = [0, 1]
    checklist = []
    def fibonacci_numbers(min):
        while True:
            next_fib = fibs[-1] + fibs[-2]
            if next_fib >= 600:
                break
            if next_fib > 20:
                checklist.append(next_fib)
            fibs.append(next_fib)
        return checklist
    def contains_fibonacci_in_string(s, limit=20):
        # Tạo danh sách các số Fibonacci nhỏ hơn 100
        if len(checklist) <= 1:
            fibonacci_list = fibonacci_numbers(limit)
        else:
            fibonacci_list = checklist
        
        # Kiểm tra từng số Fibonacci trong chuỗi
        for fib in fibonacci_list:
            if str(fib) in s:
                print("fibbbbbb")
                return True
        return False
    if action ==1:
        label = tk.Label(parent, text="Bao gồm một số Fibonacci lớn hơn 20 và nhỏ hơn 600", font=font, anchor="w", fg = 'red')
        return label
    else:
        # Kiểm tra điều kiện trong text với password
        if contains_fibonacci_in_string(password):
            return 0
        else:
            return -1


def Rule4(action, parent, font, password):
    # Hiển thị chữ thông báo yêu cầu
    dice = [1, 2, 3, 4, 5, 6]
    if action ==1:
        label = tk.Label(parent, text="Kí tự thứ 3 của mật khẩu phải là kết quả của lần tung xúc xắc ngẫu nhiên.", font=font, anchor="w", fg = 'red')
        return label
    else:
        try:
            third_char = int(password[2])  # Convert the 3rd character to integer
        except ValueError:
            return -1  # If it's not a valid number, return -1

        # Now check if the third character of password is in dice
        if third_char in dice:
            return 0  # Valid case
        else:
            return -1  # Invalid case
        
def re_captcha(event=None):
    print("Thanh cong")



def Rule5(action, parent, font, password):
    if OTP.captcha_text == 0:
        OTP.captcha_text = generate_random_string()
    print(OTP.captcha_text)
    # Tạo ảnh CAPTCHA
    image = ImageCaptcha()
    image_data = BytesIO()  # Tạo luồng nhị phân
    image.write(OTP.captcha_text, image_data)  # Ghi dữ liệu ảnh vào luồng nhị phân

    # Chuyển đổi dữ liệu nhị phân thành ảnh sử dụng Pillow
    image_data.seek(0)  # Đặt lại con trỏ của luồng để đọc từ đầu
    captcha_image = Image.open(image_data)


    captcha_photo = ImageTk.PhotoImage(captcha_image)
    # Tạo label và hiển thị CAPTCHA
    if action ==1:
        label = tk.Label(parent, text="Mật khẩu phải chứa mã captcha sau", 
                     image=captcha_photo, font=font, anchor="w", compound="bottom", fg='red')
        
        label.image = captcha_photo
        return label
    else:
        if OTP.captcha_text.upper() in password.upper():
            return 0
        else:
            return -1
        

def Rule6(action, parent, font, password):
    str = "password"
    if action ==1:
        label = tk.Label(parent, text="Không được phép chứa cụm từ 'password'", font=font, anchor="w", compound="bottom", fg='red')
        return label
    else:
        if len(password) == 0:
            return -1
        if str.upper() in password.upper():
            return -1
        else:
            return 0
        

def Rule7(action, parent, font, password):
    if action ==1:
        label = tk.Label(parent, text="Mật khẩu phải có ít nhất 1 kí tự đặc biệt", font=font, anchor="w", compound="bottom", fg='red')
        return label
    else:
        if len(password) == 0:
            return -1
        if re.search(r'[^a-zA-Z0-9\s]', password):
            return 0
        else:
            return -1


def Rule8(action, parent, font, password):
    # Hiển thị chữ thông báo yêu cầu
    str = "logic"
    if action ==1:
        label = tk.Label(parent, text="Kí tự đầu tiên và kí tự cuối cùng phải là chữ cái trong từ 'logic'", font=font, anchor="w", fg = 'red')
        return label
    else:
        if len(password) == 0:
            return -1
        if password[0] in str and password[-1] in str:
            return 0
        else:
            return -1


def Rule9(action, parent, font, password):
    so_nguyen_to = []
    def kiem_tra_nguyen_to(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def chuoi_so_nguyen_to():
        for num in range(11, 500):
            if kiem_tra_nguyen_to(num):
                so_nguyen_to.append(num)
        return so_nguyen_to
    # Hiển thị chữ thông báo yêu cầu
    str = "logic"
    if action ==1:
        label = tk.Label(parent, text="Mật khẩu phải có tổng độ dài là 1 số nguyên tố lớn hơn 10 và nhỏ hơn 500", font=font, anchor="w", fg = 'red')
        return label
    else:
        if len(password) == 0:
            return -1
        if len(password) in chuoi_so_nguyen_to():
            return 0
        else:
            return -1


def Rule10(action, parent, font, password):
    # Hiển thị chữ thông báo yêu cầu
    Week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if action ==1:
        label = tk.Label(parent, text="Mật khẩu phải bao gồm tên của một ngày trong tuần bằng tiếng anh", font=font, anchor="w", fg = 'red')
        return label
    else:
        if len(password) == 0:
            return -1
        for i in Week:
            if i.upper() in password.upper():
                return 0
        return -1
    

def Rule11(action, parent, font, password):
    def contains_consecutive_increasing_sequence(s):
        # Kiểm tra từng chuỗi con dài 4 ký tự
        for i in range(len(s) - 3):
            # Lấy 4 ký tự liên tiếp
            subsequence = s[i:i+4]
            
            # Kiểm tra xem các ký tự có phải là số và có tạo thành dãy tăng dần hay không
            if subsequence.isdigit():
                # Chuyển đổi các ký tự thành số nguyên và kiểm tra tính tăng dần
                nums = [int(ch) for ch in subsequence]
                if all(nums[j] == nums[j-1] + 1 for j in range(1, 4)):
                    return True
        return False

    # Hiển thị chữ thông báo yêu cầu
    Week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if action ==1:
        label = tk.Label(parent, text="Mật khẩu không được phép chứa 1234 hoặc dãy tăng dần liên tiếp bất kì", font=font, anchor="w", fg = 'red')
        return label
    else:
        if len(password) == 0:
            return -1
        if contains_consecutive_increasing_sequence(password):
            return -1
        return 0
    

def Rule12(action, parent, font, password):
    def check_condition(s):
        # Lọc ra các chữ số trong chuỗi
        digits = [char for char in s if char.isdigit()]
        
        # Nếu không có số nào trong chuỗi, trả về False
        if not digits:
            return False
        
        # Kiểm tra số đầu tiên trong chuỗi (số đầu tiên sau khi lọc)
        first_digit = int(digits[0])
        if first_digit % 2 == 0:
            return False
        
        # Tính tổng các số trong chuỗi
        total_sum = sum(int(digit) for digit in digits)
        
        # Kiểm tra tổng có phải là số chẵn không
        if total_sum % 2 == 0:
            return True
        else:
            return False
        
    if action ==1:
        label = tk.Label(parent, text="Chữ số đầu tiên trong mật khẩu là số lẻ nhưng tổng các chữ số là số chẵn", font=font, anchor="w", fg = 'red')
        return label
    else:
        if len(password) == 0:
            return -1
        if check_condition(password):
            return 0
        return -1