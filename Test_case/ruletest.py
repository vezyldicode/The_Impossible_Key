fibs = [0, 1]
while True:
    next_fib = fibs[-1] + fibs[-2]
    
    # Chỉ thêm vào danh sách nếu số Fibonacci lớn hơn hoặc bằng 50
    if next_fib >= 50:
        fibs.append(next_fib)
    
    # Dừng vòng lặp nếu next_fib lớn hơn hoặc bằng 600
    if next_fib >= 600:
        break

print(fibs)