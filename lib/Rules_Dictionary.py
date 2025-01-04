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

    @staticmethod
    def check_number(password):
        """Kiểm tra số"""
        return any(c.isdigit() for c in password)

    @staticmethod
    def check_special(password):
        """Kiểm tra ký tự đặc biệt"""
        return any(c in "!@#$%^&*" for c in password)

    @staticmethod
    def check_sum_10(password):
        """Kiểm tra tổng các số bằng 10"""
        numbers = [int(c) for c in password if c.isdigit()]
        return sum(numbers) == 10 if numbers else False

    @staticmethod
    def check_three_letters(password):
        """Kiểm tra có ít nhất 3 chữ cái"""
        return sum(1 for c in password if c.isalpha()) >= 3

    @staticmethod
    def check_contains_password(password):
        """Kiểm tra chứa từ 'password'"""
        return 'password' in password.lower()

    @staticmethod
    def check_even_number(password):
        """Kiểm tra có số chẵn"""
        numbers = [int(c) for c in password if c.isdigit()]
        return any(n % 2 == 0 for n in numbers)

    @staticmethod
    def check_two_special(password):
        """Kiểm tra có ít nhất 2 ký tự đặc biệt"""
        return sum(1 for c in password if c in "!@#$%^&*") >= 2

    @staticmethod
    def check_odd_length(password):
        """Kiểm tra độ dài lẻ"""
        return len(password) % 2 == 1

    @staticmethod
    def check_first_and_last_letter(password):
        #kiểm tra kí tự đầu tiên và kí tự cuối cùng
        return password[0] == password[-1]
# Danh sách tất cả các quy tắc
ALL_RULES = {
    1: ("Mật khẩu phải có ít nhất 8 ký tự", PasswordRules.check_length),
    2: ("Phải có ít nhất 1 chữ hoa", PasswordRules.check_uppercase),
    3: ("Phải có ít nhất 1 số", PasswordRules.check_number),
    4: ("Phải có ít nhất 1 ký tự đặc biệt (!@#$%^&*)", PasswordRules.check_special),
    5: ("Tổng các số trong mật khẩu phải bằng 10", PasswordRules.check_sum_10),
    6: ("Phải có ít nhất 3 chữ cái", PasswordRules.check_three_letters),
    7: ("Phải chứa từ 'password'", PasswordRules.check_contains_password),
    8: ("Phải có số chẵn", PasswordRules.check_even_number),
    9: ("Phải có ít nhất 2 ký tự đặc biệt", PasswordRules.check_two_special),
    10: ("Độ dài phải là số lẻ", PasswordRules.check_odd_length),
    11: ("Kí tự đầu tiên phải trùng với kí tự cuối cùng", PasswordRules.check_first_and_last_letter),
}