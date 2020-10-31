import numpy as np


def min_diagonal_sum(matrix):
    _, size = matrix.shape
    min_d, offset = sum(matrix.diagonal()), 0
    for i in range(-size + 2, size - 1):
        if sum(matrix.diagonal(i)) < min_d:
            min_d = sum(matrix.diagonal(i))
            offset = i
    return offset, min_d


def summ(matrix):
    res = 0
    for row in matrix:
        if all(i >= 0 for i in row):
            res += sum(row)
    return res


try:
    with open('in.txt', 'r', encoding='utf-8') as f:
        size = int(f.read())
    assert size > 0
except FileNotFoundError:
    with open('out.txt', 'w', encoding='utf-8') as f:
        f.write("Файл с входными данными не существует\n")
    exit(-1)
except Exception:
    with open('out.txt', 'w', encoding='utf-8') as f:
        f.write("Неверный ввод, ожидалось натуральное число\n")
    exit(-1)

with open('out.txt', 'w', encoding='utf-8') as f:
    matrix = np.random.randint(low=-100, high=100, size=(size, size))

    f.write(f"Матрица {size}x{size}:\n")
    f.write(f"{matrix}\n")

    f.write(f"Сумма строк с элементами >= 0: {summ(matrix)}\n")
    offset, min_d = min_diagonal_sum(matrix)
    f.write(f"Минимальная сумма элементов диагоналей, параллельных главной: {min_d}\n")
    f.write(f"{matrix.diagonal(offset)}\n")

