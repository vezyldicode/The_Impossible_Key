# rules.py

class PasswordRules:
    @staticmethod
    def check_length(password):
        """Kiểm tra độ dài tối thiểu"""
        return len(password) >= 8

    @staticmethod
    def check_uppercase(password):
        """Kiểm tra chữ hoa"""
        return any(c.isupper() for c in password)

# Danh sách tất cả các quy tắc
ALL_RULES = {
    1: ("Mật khẩu phải có ít nhất 8 ký tự", PasswordRules.check_length),
    2: ("Phải có ít nhất 1 chữ hoa", PasswordRules.check_uppercase),
}