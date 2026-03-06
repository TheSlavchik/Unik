def binary_gcd_table(a, b):
    # Заголовок таблицы
    print(f"{'Шаг':<5} | {'a (двоичный)':<16} | {'b (двоичный)':<16} | {'Действие'}")
    print("-" * 65)
    
    step = 0
    k = 0
    
    while a != 0 and b != 0:
        step += 1
        a_bin = bin(a)[2:]
        b_bin = bin(b)[2:]
        
        # 1. Если оба четные
        if a % 2 == 0 and b % 2 == 0:
            action = "2, k++"
            print(f"{step:<5} | {a_bin:>16} | {b_bin:>16} | {action}")
            a //= 2
            b //= 2
            k += 1
        # 2. Если a четное
        elif a % 2 == 0:
            action = "4.1"
            print(f"{step:<5} | {a_bin:>16} | {b_bin:>16} | {action}")
            a //= 2
        # 3. Если b четное
        elif b % 2 == 0:
            action = "4.2"
            print(f"{step:<5} | {a_bin:>16} | {b_bin:>16} | {action}")
            b //= 2
        # 4. Оба нечетные
        else:
            if a >= b:
                action = "4.3"
                print(f"{step:<5} | {a_bin:>16} | {b_bin:>16} | {action}")
                a = (a - b)
            else:
                action = "4.3"
                print(f"{step:<5} | {a_bin:>16} | {b_bin:>16} | {action}")
                b = (b - a)

    res = (a if a != 0 else b) << k
    print("-" * 65)
    print(f"Результат: {res} (в двоичной: {bin(res)[2:]})")

# Исходные данные
a_val = 203346
b_val = 48906

binary_gcd_table(a_val, b_val)
