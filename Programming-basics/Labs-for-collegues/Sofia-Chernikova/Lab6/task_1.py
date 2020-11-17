try:
    with open('task1_in.txt') as f:
        vals = f.read().split()
    a = float(vals[0])
    c = float(vals[1])
except FileNotFoundError:
    with open('task1_out.txt', 'w') as f:
        f.write("Файл со входными данными не найден")
    exit(-1)
except Exception:
    with open('task1_out.txt', 'w') as f:
        f.write("Неверный ввод, ожидались 2 числа в одной строке через пробел")
    exit(-1)

with open('task1_out.txt', 'w') as f:
    z2 = 1 - 2 * c + a
    try:
        z1 = ((1 + 6 * a * c) / (a ** 3 - 8 * c ** 3) - 1 / (a - 2 * c)) / (
                    1 / (a ** 3 - 8 * c ** 3) - 1 / (a ** 2 + 2 * a * c + 4 * c ** 2))
    except ZeroDivisionError:
        f.write("Неверный ввод, при подсчёте z1 знаменатель обратился в 0\n")
    else:
        f.write("z1 = {}\n".format(z1))
    f.write("z2 = {}\n".format(z2))
