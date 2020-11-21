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
    n, m = map(int, input("Введите размерность матрицы (NxM): ").split())
except ValueError:
    print("Ожидались два числа через пробел")
    exit(-1)

matrix = np.random.randint(low=-10, high=10, size=(n, m))
print(*matrix, sep='\n')
print('-' * 10)
print("Количество столбцов без нулей: ", count_of_columns(matrix))
print('-' * 10)
print("Отсортированная по возрастанию характеристик:")
print(*sorted(matrix, key=characteristic), sep='\n')
