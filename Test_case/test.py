def check_first_last_char(s):
    if s[0] == s[-1]:
        return 0
    return None  # Hoặc có thể trả về một giá trị khác nếu không trùng

# Ví dụ sử dụng
chuoi = "madam"
result = check_first_last_char(chuoi)
print(result)  # Kết quả: 0 nếu ký tự đầu và cuối trùng nhau