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
        return sum(numbers) >= 10 if numbers else False

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
        if len(password) <=1:
            return False
        return password[0] == password[-1]
    
    @staticmethod
    def check_vowels_count(password):
        """Kiểm tra có chính xác 3 nguyên âm"""
        vowels = 'aeiouAEIOU'
        return sum(1 for c in password if c in vowels) >= 3

    @staticmethod
    def check_consonants_count(password):
        """Kiểm tra có ít nhất 4 phụ âm"""
        consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        return sum(1 for c in password if c in consonants) >= 4

    @staticmethod
    def check_alternate_case(password):
        """Kiểm tra chữ cái xen kẽ hoa thường"""
        letters = [c for c in password if c.isalpha()]
        if len(letters) < 2:
            return False
        return all(letters[i].isupper() != letters[i+1].isupper() for i in range(len(letters)-1))

    def check_no_consecutive_same_letter(password):
        """Kiểm tra không có 2 chữ cái giống nhau liền kề (phân biệt chữ hoa và chữ thường)."""
        letters = [c for c in password if c.isalpha()]
        if len(letters) < 2:
            return True
        return all(letters[i] != letters[i + 1] for i in range(len(letters) - 1))

    @staticmethod
    def check_alphabetical_sequence(password):
        """Phải có 3 chữ cái liên tiếp theo bảng chữ cái"""
        letters = [c.lower() for c in password if c.isalpha()]
        for i in range(len(letters)-2):
            if ord(letters[i+1]) == ord(letters[i]) + 1 and ord(letters[i+2]) == ord(letters[i]) + 2:
                return True
        return False

    @staticmethod
    def check_contains_hello(password):
        """Phải chứa 'hello' với chữ cái đầu viết hoa"""
        return 'hello' in password.lower()

    @staticmethod
    def check_z_before_a(password):
        """Nếu có chữ 'z', phải có chữ 'a' đứng sau nó"""
        lower_pass = password.lower()
        z_positions = [i for i, char in enumerate(lower_pass) if char == 'z']
        for pos in z_positions:
            if pos == len(password) - 1:
                return False
            if 'a' not in lower_pass[pos+1:]:
                return False
        return True if not z_positions else True

    @staticmethod
    def check_letter_count_multiple_3(password):
        """Số lượng chữ cái phải là bội số của 3"""
        letter_count = sum(1 for c in password if c.isalpha())
        return letter_count % 3 == 0

    @staticmethod
    def check_starts_with_consonant(password):
        """Phải bắt đầu bằng phụ âm"""
        consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        return password[0] in consonants if password else False

    @staticmethod
    def check_letter_groups(password):
        """Phải có các nhóm chữ cái theo chức năng ngữ âm (ch, sh, th, wh)"""
        phonetic_groups = ['ch', 'sh', 'th', 'wh']
        return any(group in password.lower() for group in phonetic_groups)

    @staticmethod
    def check_contains_month(password):
        """Phải chứa tên của một tháng trong năm (viết tắt hoặc đầy đủ)"""
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                'january', 'february', 'march', 'april', 'june', 'july', 'august', 'september', 
                'october', 'november', 'december']
        return any(month in password.lower() for month in months)

    @staticmethod
    def check_palindrome_letters(password):
        """Các chữ cái phải tạo thành chuỗi palindrome"""
        letters = [c.lower() for c in password if c.isalpha()]
        return letters == letters[::-1]

    @staticmethod
    def check_double_letters(password):
        """Phải có ít nhất một cặp chữ cái đôi (như 'oo', 'ee')"""
        letters = [c.lower() for c in password if c.isalpha()]
        return any(letters[i] == letters[i+1] for i in range(len(letters)-1))

    @staticmethod
    def check_no_y(password):
        """Không được chứa chữ 'y' hoặc 'Y'"""
        return 'y' not in password.lower()

    @staticmethod
    def check_more_vowels_than_consonants(password):
        """Số nguyên âm phải nhiều hơn số phụ âm"""
        vowels = sum(1 for c in password.lower() if c in 'aeiou')
        consonants = sum(1 for c in password.lower() if c.isalpha() and c not in 'aeiou')
        return vowels > consonants

    @staticmethod
    def check_contains_color(password):
        """Phải chứa tên của một màu cơ bản"""
        colors = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'pink', 'purple']
        return any(color in password.lower() for color in colors)

    @staticmethod
    def check_letter_pairs(password):
        """Phải có ít nhất hai cặp chữ cái giống nhau"""
        letter_pairs = {}
        for i in range(len(password)-1):
            pair = password[i:i+2].lower()
            if pair.isalpha():
                letter_pairs[pair] = letter_pairs.get(pair, 0) + 1
        return sum(1 for count in letter_pairs.values() if count >= 2) >= 2

    @staticmethod
    def check_mirror_letters(password):
        """Phải chứa ít nhất một cặp chữ cái đối xứng (d/b, p/q, M/W, n/u)"""
        mirror_pairs = [('d','b'), ('p','q'), ('M','W'), ('n','u')]
        return any(a in password and b in password for a,b in mirror_pairs)

    @staticmethod
    def check_contains_day(password):
        """Phải chứa tên của một ngày trong tuần"""
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
               'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        return any(day in password.lower() for day in days)

    @staticmethod
    def check_letter_frequency(password):
        """Mỗi chữ cái không được xuất hiện quá 2 lần"""
        letter_count = {}
        for c in password.lower():
            if c.isalpha():
                letter_count[c] = letter_count.get(c, 0) + 1
        return all(count <= 2 for count in letter_count.values())

    @staticmethod
    def check_vowel_positions(password):
        """Nguyên âm chỉ được xuất hiện ở vị trí chẵn"""
        vowels = 'aeiouAEIOU'
        return all(c not in vowels for i, c in enumerate(password) if i % 2 == 1)

    @staticmethod
    def check_consonant_cluster(password):
        """Phải có ít nhất một cụm 3 phụ âm liên tiếp"""
        consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        count = 0
        max_count = 0
        for c in password:
            if c in consonants:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 0
        return max_count >= 3

    @staticmethod
    def check_repeating_pattern(password):
        """Phải có một mẫu chữ cái lặp lại ít nhất 2 lần"""
        letters = ''.join(c for c in password if c.isalpha()).lower()
        for length in range(2, len(letters)//2 + 1):
            for i in range(len(letters) - length):
                pattern = letters[i:i+length]
                if letters.count(pattern) >= 2:
                    return True
        return False

    @staticmethod
    def check_contains_chemical_symbol(password):
        """Phải chứa ký hiệu hóa học của một nguyên tố"""
        elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar']
        return any(element in password for element in elements)

    @staticmethod
    def check_letter_sum(password):
        """Tổng vị trí của các chữ cái trong bảng chữ cái phải là số chẵn"""
        total = sum(ord(c.lower()) - ord('a') + 1 for c in password if c.isalpha())
        return total % 2 == 0

    @staticmethod
    def check_unique_first_letters(password):
        """Chữ cái đầu tiên của mỗi từ phải khác nhau"""
        words = password.split()
        first_letters = [word[0].lower() for word in words if word and word[0].isalpha()]
        return len(first_letters) == len(set(first_letters))

    @staticmethod
    def check_contains_compass_direction(password):
        """Phải chứa một hướng la bàn (N, S, E, W, NE, SW, ...)"""
        directions = ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw', 'north', 'south', 'east', 'west']
        return any(direction in password.lower() for direction in directions)

    @staticmethod
    def check_morse_code_letter(password):
        """Phải chứa một chữ cái có thể biểu diễn bằng mã Morse dùng dấu chấm và gạch ngang trong password"""
        morse_patterns = {'a': '.-', 'b': '-...', 'e': '.', 't': '-', 's': '...', 'o': '---'}
        lower_pass = password.lower()
        return any(pattern.replace('.', '.').replace('-', '-') in lower_pass for pattern in morse_patterns.values())

    @staticmethod
    def contains_prime(password):
        """Kiểm tra có số nguyên tố"""
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
        return any(is_prime(int(c)) for c in password if c.isdigit())
    
    @staticmethod
    def has_fibonacci_sequence(password):
        """Kiểm tra có 3 số liên tiếp thuộc dãy Fibonacci"""
        nums = [int(c) for c in password if c.isdigit()]
        for i in range(len(nums)-2):
            if nums[i+2] == nums[i+1] + nums[i]:
                return True
        return False
    
    @staticmethod
    def sum_digits_even(password):
        """Tổng các chữ số phải là số chẵn"""
        return sum(int(c) for c in password if c.isdigit()) % 2 == 0
    
    @staticmethod
    def product_digits_greater_100(password):
        """Tích các chữ số phải lớn hơn 100"""
        nums = [int(c) for c in password if c.isdigit()]
        if not nums:
            return False
        product = 1
        for n in nums:
            product *= n
        return product > 100
    
    @staticmethod
    def contains_perfect_square(password):
        """Chứa ít nhất một số chính phương"""
        nums = [int(c) for c in password if c.isdigit()]
        return any(int(n ** 0.5) ** 2 == n for n in nums)
    
    @staticmethod
    def has_ascending_sequence(password):
        """Có dãy 3 số tăng dần"""
        nums = [int(c) for c in password if c.isdigit()]
        for i in range(len(nums)-2):
            if nums[i] < nums[i+1] < nums[i+2]:
                return True
        return False
    
    @staticmethod
    def contains_multiple_three(password):
        """Chứa số chia hết cho 3"""
        return any(int(c) % 3 == 0 for c in password if c.isdigit())
    
    @staticmethod
    def digit_count_prime(password):
        """Số lượng chữ số là số nguyên tố"""
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
        digit_count = sum(1 for c in password if c.isdigit())
        return is_prime(digit_count)
    
    @staticmethod
    def contains_perfect_number(password):
        """Chứa số hoàn hảo (6, 28, 496, 8128)"""
        perfect_numbers = {6, 28, 496, 8128}
        nums = [int(c) for c in password if c.isdigit()]
        return any(n in perfect_numbers for n in nums)
    
    @staticmethod
    def alternating_odd_even(password):
        """Các chữ số phải xen kẽ chẵn lẻ"""
        nums = [int(c) for c in password if c.isdigit()]
        if len(nums) < 2:
            return False
        for i in range(len(nums)-1):
            if nums[i] % 2 == nums[i+1] % 2:
                return False
        return True
    
    @staticmethod
    def contains_armstrong_number(password):
        """Chứa số Armstrong (153, 370, 371, 407)"""
        armstrong_numbers = {153, 370, 371, 407}
        nums = [int(c) for c in password if c.isdigit()]
        return any(n in armstrong_numbers for n in nums)
    
    @staticmethod
    def digit_difference_prime(password):
        """Hiệu của chữ số lớn nhất và nhỏ nhất là số nguyên tố"""
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
        nums = [int(c) for c in password if c.isdigit()]
        if len(nums) < 2:
            return False
        return is_prime(max(nums) - min(nums))


# Danh sách tất cả các quy tắc
ALL_RULES = {
    1: ("Mật khẩu phải có ít nhất 8 ký tự", PasswordRules.check_length),
    2: ("Phải có ít nhất 1 chữ hoa", PasswordRules.check_uppercase),
    3: ("Phải có ít nhất 1 số", PasswordRules.check_number),
    4: ("Phải có ít nhất 1 ký tự đặc biệt (!@#$%^&*)", PasswordRules.check_special),
    5: ("Tổng các số trong mật khẩu phải lớn hơn hoặc bằng 10", PasswordRules.check_sum_10),
    6: ("Phải có ít nhất 3 chữ cái", PasswordRules.check_three_letters),
    7: ("Phải chứa từ 'password'", PasswordRules.check_contains_password),
    8: ("Phải có số chẵn", PasswordRules.check_even_number),
    9: ("Phải có ít nhất 2 ký tự đặc biệt", PasswordRules.check_two_special),
    10: ("Độ dài phải là số lẻ", PasswordRules.check_odd_length),
    11: ("Kí tự đầu tiên phải trùng với kí tự cuối cùng", PasswordRules.check_first_and_last_letter),
    12: ("Phải có nhiều hơn 3 nguyên âm", PasswordRules.check_vowels_count),
    13: ("Phải có ít nhất 4 phụ âm", PasswordRules.check_consonants_count),
    14: ("Các chữ cái phải xen kẽ hoa thường", PasswordRules.check_alternate_case),
    15: ("Không có 2 chữ cái giống nhau liền kề", PasswordRules.check_no_consecutive_same_letter),
    16: ("Phải có 3 chữ cái liên tiếp theo bảng chữ cái", PasswordRules.check_alphabetical_sequence),
    17: ("Phải chứa 'Hello'", PasswordRules.check_contains_hello),
    18: ("Nếu có chữ 'z', phải có chữ 'a' đứng sau nó", PasswordRules.check_z_before_a),
    19: ("Số lượng chữ cái phải là bội số của 3", PasswordRules.check_letter_count_multiple_3),
    20: ("Phải bắt đầu bằng phụ âm", PasswordRules.check_starts_with_consonant),
    21: ("Phải có các nhóm chữ cái theo chức năng ngữ âm (ch, sh, th, wh)", PasswordRules.check_letter_groups),
    22: ("Phải chứa tên của một tháng", PasswordRules.check_contains_month),
    23: ("Các chữ cái phải tạo thành chuỗi palindrome", PasswordRules.check_palindrome_letters),
    24: ("Phải có ít nhất một cặp chữ cái đôi", PasswordRules.check_double_letters),
    25: ("Không được chứa chữ 'y'", PasswordRules.check_no_y),
    26: ("Số nguyên âm phải nhiều hơn số phụ âm", PasswordRules.check_more_vowels_than_consonants),
    27: ("Phải chứa tên của một màu cơ bản", PasswordRules.check_contains_color),
    28: ("Phải có ít nhất hai cặp chữ cái giống nhau", PasswordRules.check_letter_pairs),
    29: ("Phải chứa ít nhất một cặp chữ cái đối xứng (d/b, p/q, M/W, n/u)", PasswordRules.check_mirror_letters),
    30: ("Phải chứa ít nhất một số nguyên tố", PasswordRules.contains_prime),
    31: ("Phải có 3 số liên tiếp thuộc dãy Fibonacci", PasswordRules.has_fibonacci_sequence),
    32: ("Tổng các chữ số phải là số chẵn", PasswordRules.sum_digits_even),
    44: ("Tích các chữ số phải lớn hơn 100", PasswordRules.product_digits_greater_100),
    34: ("Phải chứa ít nhất một số chính phương", PasswordRules.contains_perfect_square),
    35: ("Phải có dãy 3 số tăng dần", PasswordRules.has_ascending_sequence),
    36: ("Phải chứa số chia hết cho 3", PasswordRules.contains_multiple_three),
    37: ("Số lượng chữ số phải là số nguyên tố", PasswordRules.digit_count_prime),
    38: ("Phải chứa một số hoàn hảo (6, 28, 496, 8128)", PasswordRules.contains_perfect_number),
    39: ("Các chữ số phải xen kẽ chẵn lẻ", PasswordRules.alternating_odd_even),
    40: ("Phải chứa một số Armstrong (153, 370, 371, 407)", PasswordRules.contains_armstrong_number),
    41: ("Hiệu của chữ số lớn nhất và nhỏ nhất phải là số nguyên tố", PasswordRules.digit_difference_prime),
}