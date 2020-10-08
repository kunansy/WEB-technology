import random


try:
    N = int(input("Введите длину массива (натуральное число <= 30): "))
    assert 0 < N <= 30
except ValueError:
    print("Ожидалось натуральное число")
    exit(-1)
except AssertionError:
    print("Ожидалось натуральное число не больше 30")
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

print(f"Длина массива: {N}")
print('Массив:', '\n', values)
print(f"Произведение отрицательных элементов: {mult_of_negative}")
print(f"Сумма положительных до максимума: {sum_after_max}")
print('Перевёрнутый массив', '\n', reversed_values)
