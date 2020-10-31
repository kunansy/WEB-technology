import random


try:
    with open('in.txt', 'r', encoding='utf-8') as f:
        N = int(f.read())
    assert 0 < N <= 30
except FileNotFoundError:
    with open('out.txt', 'w', encoding='utf-8') as f:
        f.write('Файл с входными данными не существует')
        exit(-1)
except Exception:
    with open('out.txt', 'w', encoding='utf-8') as f:
        f.write("Ожидалось натуральное число")
        exit(-1)

values = [random.uniform(-5, 5) for i in range(N)]

mult_of_negative = 1
for item in values:
    if item < 0:
        mult_of_negative *= item

max_ = max(values)
max_index = values.index(max_)
sum_after_max = 0
for item in values[:max_index]:
    if item > 0:
        sum_after_max += item

reversed_values = values[::-1]

with open('out.txt', 'w', encoding='utf-8') as f:
    f.write(f"Длина массива: {N}\n")
    f.write(f"Массив:\n{values}\n")
    f.write(f"Произведение отрицательных элементов: {mult_of_negative}\n")
    f.write(f"Сумма положительных до максимума: {sum_after_max}\n")
    f.write(f"Перевёрнутый массив\n{reversed_values}\n")

