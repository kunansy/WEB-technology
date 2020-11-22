from random import uniform


def sum_of_positive_nums(arr):
    res = 0
    for i in arr:
        if i > 0:
            res += i
    return res


def max_by_abs(arr):
    mmax = None
    for i in arr:
        if mmax is None or abs(i) > abs(mmax):
            mmax = i
    return mmax


def min_by_abs(arr):
    mmin = None
    for i in arr:
        if mmin is None or abs(i) < abs(mmin):
            mmin = i
    return mmin


try:
    with open("in.txt") as file:
        n = int(file.read())
except FileNotFoundError:
    with open("out.txt", 'w', encoding='utf-8') as file:
        file.write("Файл с входными данными не найден")
    exit(-1)
except ValueError:
    with open("out.txt", 'w', encoding='utf-8') as file:
        file.write("Ожидалось число")
    exit(-1)

arr = []
for _ in range(n):
    val = round(uniform(-5, 5), 2)
    arr.append(val)

with open("out.txt", 'w', encoding='utf-8') as file:
    for i in arr:
        file.write(f"{i}, ")
    file.write('\n')
    file.write(f"Сумма положительных элементов = {sum_of_positive_nums(arr)}\n")
    arr.sort(reverse=True)

    mmax = max_by_abs(arr)
    mmin = min_by_abs(arr)
    mult = 1

    for i in arr[arr.index(mmax):arr.index(mmin) + 1]:
        mult *= i
    file.write(f"Произведение: {mult}\n")
    file.write("Отсортированный массив:\n")
    for i in arr:
        file.write(f"{i}, ")
