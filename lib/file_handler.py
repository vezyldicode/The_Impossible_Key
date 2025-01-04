# Thư viện quản lý và điều khiển xuất nhập tệp
# Date 14.12.2024
# Author: Vezyldicode

import os


def fread(file_path):
    # Đọc toàn bộ nội dung file
    # return content nếu file được đọc thành công, nếu lỗi return -1, hoặc tệp không tồn tại return 0
    try:
        with open(file_path, 'r') as file:
            content = file.read() 
            return content
    except FileNotFoundError:
        return 0
    except Exception as e:
        return -1


def fcreate(file_path):
    # tạo 1 file mới
    # return 1 nếu file được tạo thành công, nếu lỗi return -1, hoặc tệp đã tồn tại return 0
    try:
        with open(file_path, 'x') as file:
            file.write("")
        return 1
    except FileExistsError:
        return 0
    except Exception as e:
        return -1


def fwrite(file_path, content):
    # Ghi nội dung vào tệp
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return 1
    except Exception as e:
        return -1


def fappend(file_path, content):
    # Ghi nội dung vào tệp
    try:
        with open(file_path, 'a') as file:
            file.write(f"{content}\n")
        return 1
    except Exception as e:
        return -1


def fsreach(file_path, keyword):
    # Đọc file và tìm giá trị sau dấu '=' của từ khoá
    # return value nếu tìm thấy giá trị, return -1 nếu tệp không tồn tại hoặc lỗi khác, return "" nếu không có tìm thấy từ khoá
    try:
        with open(file_path, 'r') as file:  # Mở tệp trong chế độ đọc
            for line in file:  # Duyệt qua từng dòng trong tệp
                if keyword in line:  # Kiểm tra xem từ khóa có trong dòng không
                    # Tách giá trị sau dấu '=' và loại bỏ khoảng trắng
                    parts = line.split('=')  
                    if len(parts) > 1:
                        value = parts[1].strip()  # Lấy phần sau dấu '=' và loại bỏ khoảng trắng
                        return value
        return "" #f"Từ khóa '{keyword}' không tìm thấy trong tệp."
    except FileNotFoundError:
        return -1
    except Exception as e:
        return 0 #f"Lỗi: {e}"


def fdelete(file_path):
    try:
        os.remove(file_path)  # Xóa tệp
        return f"Tệp {file_path} đã được xóa."
    except FileNotFoundError:
        return f"Tệp {file_path} không tồn tại."
    except Exception as e:
        return f"Lỗi: {e}"