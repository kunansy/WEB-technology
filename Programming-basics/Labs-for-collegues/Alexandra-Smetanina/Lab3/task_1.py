from math import sqrt


def f(x):
    if x < -1:
        return -x - 1
    elif -1 <= x < 1:
        return 0
    elif 1 <= x < 5:
        return sqrt(4 - (x - 3)**2)
    else:
        return (-x + 5) / 2

try:
    start = float(input("Введите Хнач: "))
    stop = float(input("Введите Хконц: "))
    step = float(input("Введите шаг: "))
except ValueError:
    print("Ожидались числа")
    exit(-1)

print("+--------+--------+")
print("|   X    |    Y   |")
print("+--------+--------+")

cycle_var = start
while cycle_var <= stop:
    x = f"{cycle_var:.1f}".ljust(5).rjust(8)
    y = f"{f(cycle_var):.1f}".ljust(5).rjust(8)

    print(f"|{x}|{y}|")

    cycle_var += step
print("+--------+--------+")
