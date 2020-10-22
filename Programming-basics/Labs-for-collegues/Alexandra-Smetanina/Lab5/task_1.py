import colorama
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


def justify(s):
    return str(s).rjust(3).ljust(3)


def highlight_diagonal(matrix, offset):
    _, size = matrix.shape
    is_d = lambda n, m: n + offset == m
    for row in range(size):
        for i in range(size):
            if is_d(row, i):
                out = str(matrix[row][i])
                print(colorama.Fore.GREEN, justify(out), sep='', end=' ')
                print(colorama.Fore.RESET, end='', sep='')
            else:
                print(justify(matrix[row][i]), end=' ', sep='')
        print()


def print_matrix(matrix):
    for row in matrix:
        print(' '.join(justify(i) for i in row))


def main():
    try:
        size = int(input("Введите размерность матрицы: "))
        assert size > 0
    except ValueError:
        print("Неверный ввод, ожидалось натуральное число")
        return
    except AssertionError:
        print("Неверный ввод, ожидалось натуральное число")
        return
    matrix = np.random.randint(low=-100, high=100, size=(size, size))
    print(f"Матрица {size}x{size}: ")
    print_matrix(matrix)
    print(f"Сумма строк с элементами >= 0: {summ(matrix)}")
    offset, min_d = min_diagonal_sum(matrix)
    print(f"Мин сумма элементов диагоналей, || главной: {min_d}")
    print("Которая находится: ")
    highlight_diagonal(matrix, offset)


if __name__ == "__main__":
    main()
