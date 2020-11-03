from math import sin, cos, pi


def f():
    with open('in.txt', 'r', encoding='utf-8') as f:
        a = float(f.read())
    z1 = (((1 + a + a**2) / (2 * a + a**2)) + 2 - ((1 - a + a**2) / (2 * a - a**2))) * (5 - 2 * a**2)
    z2 = (4 - a**2) / 2
    with open('out.txt', 'w', encoding='utf-8') as f:
        f.write(f"z1 = {z1:.4f}\n")
        f.write(f"z2 = {z2:.4f}\n")


try:
    f()
except FileNotFoundError:
    with open('out.txt', 'w', encoding='utf-8') as f:
        f.write("Файл со входными данными не найден\n")
except ZeroDivisionError:
    with open('out.txt', 'w', encoding='utf-8') as f:
        f.write("Введено неверное число, произошло деление на 0\n")
except Exception:
    with open('out.txt', 'w', encoding='utf-8') as f:
        f.write("Ожидалось вещественное число")

