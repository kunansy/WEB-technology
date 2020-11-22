from math import (cos, sin, sqrt, pi)


def f():
    try:
        with open("in.txt") as file:
            a = float(file.read())
    except FileNotFoundError:
        with open("out.txt", 'w', encoding='utf-8') as file:
            file.write("Нет файла с данными!")
        exit(-1)
    except ValueError:
        with open("out.txt", 'w', encoding='utf-8') as file:
            file.write('Передано неверное значение, ожидалось число')
        exit(-1)

    z1 = cos(a) + sin(a) + cos(3*a) + sin(3*a)
    z2 = 2 * sqrt(2) * cos(a) * sin(pi/4 + 2 * a)

    with open('out.txt', 'w', encoding='utf-8') as file:
        file.write(f"z1 = {z1}\nz2 = {z2}")


f()
