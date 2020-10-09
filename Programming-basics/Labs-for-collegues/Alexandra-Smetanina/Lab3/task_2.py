import random


def f(x, y, r):
    if x * y < 0:
        return False
    if x > 0:
        if x > 2 * r or y > 2 * r:
            return False
        return x**2 + y**2 >= r**2
    return y >= -2 * r - x


try:
    R = float(input("Введите радиус: "))
except ValueError:
    print("Ожидалось число")
    exit(-1)

print("+--------+--------+----------+")
print("|   X    |    Y   |  Попала  |")
print("+--------+--------+----------|")
for _ in range(10):
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    result = f(x, y, R)

    x = f"{x:.1f}".ljust(5).rjust(8)
    y = f"{y:.1f}".ljust(5).rjust(8)
    result = f"{result}".ljust(7).rjust(10)
    print(f"|{x}|{y}|{result}|")
print("+--------+--------+----------+")
