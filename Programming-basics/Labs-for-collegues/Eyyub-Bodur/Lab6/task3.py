import numpy as np


def characteristic(row):
    res = 0
    for i in row:
        if i > 0 and i % 2 == 0:
            res += i
    return res


def count_of_columns(matrix):
    _, columns = matrix.shape
    count = 0
    for column in range(columns):
        if all(matrix[:, column]):
            count += 1
    return count


try:
    with open("in.txt") as file:
        n, m = map(int, file.read().split())
except FileNotFoundError:
    with open("out.txt", 'w', encoding='utf-8') as file:
        file.write("Файл со входными данными не найден")
    exit(-1)
except ValueError:
    with open("out.txt", 'w', encoding='utf-8') as file:
        file.write("Ожидались два числа через пробел")
    exit(-1)

matrix = np.random.randint(low=-10, high=10, size=(n, m))
with open("out.txt", "w", encoding='utf-8') as file:
    for row in matrix:
        file.write(f"{row}\n")
    file.write('-' * 10 + '\n')
    file.write(f"Количество столбцов без нулей: {count_of_columns(matrix)}\n")
    file.write('-' * 10 + '\n')
    file.write("Отсортированная по возрастанию характеристик:\n")
    for row in sorted(matrix, key=characteristic):
        file.write(f"{row}\n")
