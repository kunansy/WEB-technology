from random import randint


def print_matrix(f, m1, m2, m3, m4):
    for i in range(N):
        f.write(' '.join(str(num) for num in m1[i]) + '|')
        f.write(' '.join(str(num) for num in m2[i]) + '\n')
    f.write("- - - - - - - - - - - - - - -\n")
    for i in range(N):
        f.write(' '.join(str(num) for num in m3[i]) + '|')
        f.write(' '.join(str(num) for num in m4[i]) + '\n')
    f.write('\n')


def print_sum(f, m1, m2, m3, m4):
    f.write("Сумма 1 элемента = {}\n".format(ssum(m1)))
    f.write("Сумма 2 элемента = {}\n".format(ssum(m2)))
    f.write("Сумма 3 элемента = {}\n".format(ssum(m3)))
    f.write("Сумма 4 элемента = {}\n".format(ssum(m4)))


def ssum(mat):
    return sum(sum(i) for i in mat)


def create_matrix(size):
    return [
        [randint(10, 20) for _ in range(size)]
        for _ in range(size)
    ]


with open("task3_out.txt", 'w') as f:
    try:
        with open('task3_in.txt') as fin:
            N = int(fin.read())
    except FileNotFoundError:
        f.write("Файл со входными данными не найден")
        exit(-1)
    except ValueError:
        f.write("Ожидалось число")
        exit(-1)

    mat1 = create_matrix(N)
    mat2 = create_matrix(N)
    mat3 = create_matrix(N)
    mat4 = create_matrix(N)

    # Вывод начального состояния матрицы и суммы на начальном состоянии
    f.write("Начальное состояние: \n")
    print_matrix(f, mat1, mat2, mat3, mat4)

    f.write("Сумма элементов на начальном состоянии: \n")
    print_sum(f, mat1, mat2, mat3, mat4)

    # Преобразования внутри матрицы
    for i in range(N):
        for j in range(N):
            mat1[i][j], mat2[i][j] = mat2[i][j], mat1[i][j]
            mat3[i][j], mat4[i][j] = mat4[i][j], mat3[i][j]
            mat1[i][j], mat4[i][j] = mat4[i][j], mat1[i][j]

    # Вывод конечного состояния матрицы и суммы на конечном состоянии
    f.write("Конечное состояние: \n")
    print_matrix(f, mat1, mat2, mat3, mat4)
    print_sum(f, mat1, mat2, mat3, mat4)
