from random import uniform


def print_list(l):
    return ' '.join("{0:.2f}".format(i) for i in sorted(mas))


with open('task2_out.txt', 'w') as f:
    # Ввод количества элементов списка
    try:
        with open('task2_in.txt') as fin:
            n = int(fin.read())
    except FileNotFoundError:
        f.write("Файл со входными даными не найден")
        exit(-1)
    except ValueError:
        f.write("Ожидалось целое число не больше 30")
        exit(-1)

    if n > 30:
        n = 30
    elif n < 5:
        n = 5

    # Генерация и вывод начального состояния списка (массива)
    mas = []
    for i in range(n):
        mas.append(uniform(-10, 10))

    f.write("Начальное состояние:\n")
    f.write(print_list(mas))

    # Поиск второго максимума
    max1 = mas[0]
    max2 = mas[0]
    for i in range(1, n):
        if max1 < mas[i]:
            max2 = max1
            max1 = mas[i]
        elif max2 < mas[i]:
            max2 = mas[i]
    f.write("\nВторой максимум:\n")
    f.write("{0:.3f}\n".format(max2))
    # Сумма элементов
    mas.index(max1)
    mas.index(max2)
    if mas.index(max1) < mas.index(max2):
        q = mas.index(max1) + 1
        z = mas.index(max2)
    else:
        q = mas.index(max2) + 1
        z = mas.index(max1)

    ssum = 0
    for i in range(q, z):
        ssum = ssum + mas[i]
    f.write("Сумма:\n")
    f.write("{0:.3f}\n".format(ssum))

    # Вывод конечного состояния списка
    f.write('Конечное состояние:\n')
    f.write(print_list(mas))
